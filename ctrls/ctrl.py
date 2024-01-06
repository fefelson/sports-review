"""
    NOT A REAL model
    PLACEHOLDER FOR TEMPORARY PURPOSES
"""


class Ctrl:

    def __init__(self):

        self.league = League()
        self.frame = FelsonFrame()
        self.focusedGame = None


    def onClick(self, evt):
        gameId = evt.GetEventObject().GetName()
        game = self.league.games[gameId]


        awayFrame = wx.Frame(None)
        awaySizer = wx.BoxSizer()
        awayPanel = TitlePanel(awayFrame)
        awayPanel.bind(self.titleClick)
        awayPanel.setPanel(game=game, hA="away")
        awaySizer.Add(awayPanel)
        awayFrame.SetSizer(awaySizer)
        awayFrame.Fit()
        awayFrame.Show()

        # put bindings in better place
        for widge in [awayPanel.matchupPanel.values[hA] for hA in ("away", "home")]:
            widge.Bind(wx.EVT_LEFT_DCLICK, self.onMoney)

        awayPanel.matchupPanel.spread.Bind(wx.EVT_LEFT_DCLICK, self.onSpread)
        awayPanel.matchupPanel.ou.Bind(wx.EVT_LEFT_DCLICK, self.onOU)

        homeFrame = wx.Frame(None)
        homeSizer = wx.BoxSizer()
        homePanel = TitlePanel(homeFrame)
        homePanel.bind(self.titleClick)
        homeLog = GameLogPanel(homeFrame)
        homePanel.setPanel(game=game, hA="home")
        homeLog.setPanel(game.getTeam("home").getGameLog(), game.getTeam("home").getActiveIds(), )
        homeSizer.Add(homePanel)
        homeSizer.Add(homeLog)
        homeFrame.SetSizer(homeSizer)
        homeFrame.Fit()
        homeFrame.Show()

        # put bindings in better place
        for widge in [homePanel.matchupPanel.values[hA] for hA in ("away", "home")]:
            widge.Bind(wx.EVT_LEFT_DCLICK, self.onMoney)

        homePanel.matchupPanel.spread.Bind(wx.EVT_LEFT_DCLICK, self.onSpread)
        homePanel.matchupPanel.ou.Bind(wx.EVT_LEFT_DCLICK, self.onOU)


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
