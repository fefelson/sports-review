"""
    NOT A REAL model
    PLACEHOLDER FOR TEMPORARY PURPOSES
"""


class Ctrl:

    def __init__(self):

        self.league = League()
        self.frame = FelsonFrame()
        self.focusedGame = None


    def getGameStats(self, event):
        gameId, oppId = event.GetEventObject().GetName().split()
        req = self.league.getGameStats(gameId, oppId)
        worker = GameStatsThread(self.statsPanel, self.league.dB.run, req)
        worker.setResultType(BasketballTeamStats)
        worker.start()


    def onCollapse(self, event):
        if event.GetEventObject().IsExpanded():
            for game in self.panel.panels.values():
                game.isActive.Show()
                game.Layout()
        else:
            for game in self.panel.panels.values():
                game.isActive.Hide()
                game.Layout()
        self.panel.Layout()


    def getOverview(self):
        req = self.league.overview.getOverview()
        worker = OverviewThread(self.panel, self.league.dB.run, req)
        worker.start()
