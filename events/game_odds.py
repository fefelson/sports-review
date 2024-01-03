import statistics

from threading import Thread
from wx import NewEventType, PostEvent, PyEventBinder, PyCommandEvent


myEVT_GameOdds = NewEventType()
EVT_GameOdds = PyEventBinder(myEVT_GameOdds)


def setROI(games, *, roiType="MONEY"):
    total = len(games)*100
    subTotal = 0
    teamSlug = ""

    if roiType == "MONEY":
        for game in games:
            if game["{}MoneyOut".format(teamSlug)] > 0 and isinstance(game["{}ML".format(teamSlug)], int):

                if game["{}ML".format(teamSlug)] > 0:
                    subTotal += round(game["{}ML".format(teamSlug)]+100,2)
                else :
                    subTotal += round((10000/(game["{}ML".format(teamSlug)]*-1))+100,2)

    elif roiType == "ATS":
        for game in games:
            if game["{}SpreadOut".format(teamSlug)] > 0:
                subTotal += round((1000/11)+100,2)
            elif game["{}SpreadOut".format(teamSlug)] == 0:
                subTotal += 100
    roi = (subTotal - total) / total *100
    return roi

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

    def __init__(self, parent, dbRun, req):
        """@param parent: The gui object that should recieve the value
           @param req: the Request object to send to the dB
           @param dbRun: dB.run function to be threaded
        """
        Thread.__init__(self)
        self.dbRun = dbRun
        self._parent = parent
        self._req = req
        self.resultType = None


    def setResultType(self, resultType):
        self.resultType = resultType


    def run(self):
        self.dbRun(self._req)
        answer = self._req.value

        result = {"away":{}, "home":{}}
        # type specific object
        if self.resultType:
            self.resultType(answer)

        else:
            total = len(answer)
            result["gp"] = total
            print(total)
            for hA in ("away", "home"):
                ML = answer[0]["{}ML".format(hA)]
                wins = sum([item["{}Win".format(hA)] for item in answer if item["{}Win".format(hA)] == 1])
                covers = sum([item["{}Cover".format(hA)] for item in answer if item["{}Cover".format(hA)] == 1])
                result[hA]["ML"] =  ML if ML  < 0 else "+"+str(ML)
                result[hA]["cover%"] = covers /len(answer)*100
                result[hA]["win%"] = wins /len(answer)*100

                print(ML, wins, covers)
                if ML > 0:
                    result[hA]["winROI"] = (((ML+100)*wins)-(total*100))/total
                elif ML <0:
                    result[hA]["winROI"] = (((  (1000/ML*-1)  +100)*wins)-(total*100))/total
                print(result[hA]["winROI"])

                if ML > 0:
                    result[hA]["winROI"] = (((ML+100)*wins)-(total*100))/total
                elif ML <0:
                    result[hA]["winROI"] = (((  (1000/ML*-1)  +100)*wins)-(total*100))/total

                result[hA]["coverROI"] = ((covers*191.91)-(total*100))/total

                print(result[hA]["coverROI"])



        evt = GameOddsEvent(myEVT_GameOdds, -1, result)
        PostEvent(self._parent, evt)
