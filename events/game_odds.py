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
        result = answer if not self.resultType else self.resultType(answer)
        evt = GameStatsEvent(myEVT_GameOdds, -1, result)
        PostEvent(self._parent, evt)
