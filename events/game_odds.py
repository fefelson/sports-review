import statistics

from collections import Counter
from threading import Thread
from wx import NewEventType, PostEvent, PyEventBinder, PyCommandEvent

from ..helpers import countResults, getRequest


myEVT_GameOdds = NewEventType()
EVT_GameOdds = PyEventBinder(myEVT_GameOdds)


class GameOddsEvent(PyCommandEvent):
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


class GameOddsThread(Thread):

    def __init__(self, parent, league, gameId, hA):
        """@param parent: The gui object that should recieve the value
           @param req: the Request object to send to the dB
           @param dbRun: dB.run function to be threaded
        """
        Thread.__init__(self)
        self._parent = parent
        self._league = league
        self._gameId = gameId
        self._hA = hA


    def run(self):
        result = {}
        game = self._league.games[self._gameId]
        team = game.getTeam(self._hA)
        result["hA"] = self._hA
        result["fullName"] = team.getInfo("lastName")

        awayML = game.odds.getItem("money", "awayML")
        homeML = game.odds.getItem("money", "homeML")
        teamML = game.odds.getItem("money", "{}ML".format(self._hA))
        spread = game.odds.getItem("spread", "{}Spread".format(self._hA))
        oU = game.odds.getItem("total", "total")

        result["awayML"] = awayML
        result["homeML"] = homeML
        result["teamML"] = teamML
        result["spread"] = spread
        result["oU"] = oU


        postLines = []
        book = game.odds.getBook()

        for g in book["money"]:
            if g["{}ML".format(self._hA)]:
                temp = float( g["{}ML".format(self._hA)])
                postLines.append(temp)
        result["postLines"] = postLines



        req = getRequest(homeML=homeML, awayML=awayML)
        self._league.dB.run(req)
        result["homeMoney/awayMoney"] = countResults(req.value)

        req = getRequest(teamML=teamML, hA=self._hA)
        self._league.dB.run(req)
        result["teamMoney"] = countResults(req.value)

        evt = GameOddsEvent(myEVT_GameOdds, -1, result)
        PostEvent(self._parent, evt)
