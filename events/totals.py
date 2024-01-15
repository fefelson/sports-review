import statistics

from collections import Counter
from threading import Thread
from wx import NewEventType, PostEvent, PyEventBinder, PyCommandEvent

from ..models import Request
from ..sql import mLHistoryCmd

myEVT_Total = NewEventType()
EVT_Total = PyEventBinder(myEVT_Total)


class TotalEvent(PyCommandEvent):
    """
    Creates a new wxpython event
    The event is binded to the panel that will be
    set with a GameStats object
    """
    def __init__(self, etype, eid=-1, value=None):
        """Creates the event object"""
        PyCommandEvent.__init__(self, etype, eid)
        self._value = value

    def GetValue(self):
        """Returns the value from the event.
        @return: the value of this event

        """
        return self._value


class TotalThread(Thread):

    def __init__(self, parent, league, gameId):
        """@param parent: The gui object that should recieve the value
           @param req: the Request object to send to the dB
           @param dbRun: dB.run function to be threaded
        """
        Thread.__init__(self)
        self._parent = parent
        self._league = league
        self._gameId = gameId


    def getRequest(self, *, awayML=None, homeML=None, teamML=None, awaySpread=None, homeSpread=None, spread=None, total=None):

        andCmd = ""
        if awayML:
            andCmd += " AND away.money = ? "
        if homeML:
            andCmd += " AND home.money = ? "
        if teamML:
            andCmd += " AND {}.money = ? ".format(self._hA)
        if awaySpread:
            andCmd += " AND away.spread = ? "
        if homeSpread:
            andCmd += " AND home.spread = ? "
        if spread:
            andCmd += " AND {}.spread = ? ".format(self._hA)
        if total:
            andCmd += " AND ou = ? "

        req = Request()
        args = []
        for value in (awayML, homeML, teamML, awaySpread, homeSpread, spread, total):
            if value:
                args.append(value)

        req.args = tuple(args)
        req.stats = "median"
        req.callback = None
        req.cmd = mLHistoryCmd.format(andCmd)
        req.fetch = "fetchAll"
        req.labels =  ("homeML", "homeWin", "homeCover", "homeSpread", "homeResult",
                        "awayML", "awayWin", "awayCover", "awaySpread", "awayResult",
                        "oU", "ouOutcome", "total")

        return req

    def run(self):
        result = {}
        game = self._league.games[self._gameId]

        awayML = game.odds.getItem("money", "awayML")
        homeML = game.odds.getItem("money", "homeML")
        spread = game.odds.getItem("spread", "{}Spread".format("home"))
        oU = game.odds.getItem("total", "total")

        result["awayML"] = awayML
        result["homeML"] = homeML
        result["spread"] = spread
        result["oU"] = oU


        postLines = []
        book = game.odds.getBook()

        for g in book["total"]:
            if g["total"]:
                temp = float( g["total"])
                postLines.append(temp)
        result["postLines"] = postLines



        req = self.getRequest(homeML=homeML, awayML=awayML, total=oU)
        self._league.dB.run(req)
        try:
            result["homeMoney/awayMoney"] = self.countResults(req.value, req.stats)
        except:
            result["homeMoney/awayMoney"] = None

        req = self.getRequest(total=oU)
        self._league.dB.run(req)

        result["teamTotal"] = self.countResults(req.value, req.stats)


        evt = TotalEvent(myEVT_Total, -1, result)
        PostEvent(self._parent, evt)


    def countResults(self, answer, stats="median"):

        total = len(answer)
        result = {"away":{}, "home":{}}
        result["gp"] = total

        for hA in ("away", "home"):

            if stats == "mean":
                ML = statistics.mean([int(x["{}ML".format(hA)]) for x in answer if x["{}ML".format(hA)]])
            elif stats == "median":
                ML = statistics.median([int(x["{}ML".format(hA)]) for x in answer if x["{}ML".format(hA)]])


            overs = sum([item["ouOutcome"] for item in answer if item["ouOutcome"] == 1])
            unders = sum([1 for item in answer if item["ouOutcome"] == -1])

            spreadBoxes  = [x["total"] for x in answer]
            result[hA]["ML"] =  int(ML) if int(ML)  < 0 else "+"+str(int(ML))
            result[hA]["spreadCount"] = Counter(spreadBoxes)
            result[hA]["spreadBoxes"] = spreadBoxes

            result[hA]["over%"] = overs / total*100
            result[hA]["under%"] = unders / total*100

            result[hA]["oU"] = statistics.median([x["oU"] for x in answer if x["oU"]])
            result[hA]["total"] = statistics.median([x["total"] for x in answer if x["total"]])


            result[hA]["overROI"] = ((overs*191.91)-total*100)/total
            result[hA]["underROI"] = ((unders*191.91)-total*100)/total
        return result
