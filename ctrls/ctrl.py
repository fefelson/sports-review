"""
    NOT A REAL model
    PLACEHOLDER FOR TEMPORARY PURPOSES
"""


class Ctrl:

    def __init__(self):

        self.league = League()
        self.frame = FelsonFrame()
        self.focusedGame = None


    def onMoney(self, evt):
        print("Money", evt.GetEventObject().GetName())
        self.oddsFrame = GameOddsFrame(None)
        self.oddsFrame.Show()
        gameId = evt.GetEventObject().GetName()

        req = self.league.getOddsView(gameId)
        worker = GameOddsThread(self.oddsFrame, self.league.dB.run, req)
        worker.start()


    def onSpread(self, evt):
        print("Spread", evt.GetEventObject().GetName())
        self.spreadFrame = PointSpreadFrame(None)
        self.spreadFrame.Show()
        gameId = evt.GetEventObject().GetName()

        req = self.league.getSpreadView(gameId)
        worker = PointSpreadThread(self.spreadFrame, self.league.dB.run, req)
        worker.start()


    def onTotal(self, evt):
        print("O/U", evt.GetEventObject().GetName())
        self.totalFrame = TotalFrame(None)
        self.totalFrame.Show()
        gameId = evt.GetEventObject().GetName()

        req = self.league.getTotalView(gameId)
        worker = TotalThread(self.totalFrame, self.league.dB.run, req)
        worker.start()
