import statistics

from threading import Thread
from wx import NewEventType, PostEvent, PyEventBinder, PyCommandEvent


myEVT_Possessions = NewEventType()
EVT_Possessions = PyEventBinder(myEVT_Possessions)


class PossessionsEvent(PyCommandEvent):
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


class PossessionsThread(Thread):

    def __init__(self, parent, team):
        """@param parent: The gui object that should recieve the value
           @param req: the Request object to send to the dB
           @param dbRun: dB.run function to be threaded
        """
        Thread.__init__(self)
        self.team = team
        self._parent = parent


    def run(self):
        evt = PossessionsEvent(myEVT_Possessions, -1, self.team)
        PostEvent(self._parent, evt)
