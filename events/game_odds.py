import statistics

from threading import Thread
from wx import NewEventType, PostEvent, PyEventBinder, PyCommandEvent


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

                result[hA]["spread"] = statistics.median([x["{}Spread".format(hA)] for x in answer])
                result[hA]["result"] = statistics.median([x["{}Result".format(hA)] for x in answer])

                if ML > 0:
                    result[hA]["winROI"] = (((ML+100)*wins)-total*100)/total
                elif ML <0:
                    result[hA]["winROI"] = (((  (10000/ML*-1)  +100)*wins)-total*100)/total
                print(result[hA]["winROI"])

                result[hA]["coverROI"] = ((covers*191.91)-total*100)/total





        evt = GameOddsEvent(myEVT_GameOdds, -1, result)
        PostEvent(self._parent, evt)
