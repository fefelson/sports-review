from queue import Queue
from threading import Thread, Event




# Sentinel used for shutdown
class ThreadExit(Exception):
    pass


class Request:
    # Object to handle DB requests

    def __init__(self):

        self.args = None
        self.callback = None
        self.cmd = None
        self.fetch = None
        self.labels = None
        self.value = None


    def queryResponse(self, info):
        if self.fetch == "fetchOne":
            self.value = dict(zip(self.labels, info))
        elif self.fetch == "fetchAll":
            self.value = [dict(zip(self.labels, i)) for i in info]
        elif self.fetch == "fetchItem":
            self.value = info

        # print(self.cmd)
        # print("\n\n")
        # print(self.args)
        # print("\n\n")
        # print(self.value)
        # print("\n\n\n\n")

        if self.callback:
            self.callback(self.value)



class ThreadedDB:

    def __init__(self, felsonDB):

        self._db = felsonDB()
        self._running = False


    def run(self, req):
        assert isinstance(req, Request)
        if self._running == False:
            self._running = True
            self._db.openDB()
            if req.args:
                response = getattr(self._db, req.fetch)(req.cmd, req.args)
            else:
                response = getattr(self._db, req.fetch)(req.cmd)
            self._db.closeDB()
            req.queryResponse(response)
            self._running = False
