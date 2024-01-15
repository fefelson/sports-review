import wx

from .options_panel import OptionsPanel

from FelsonSports import Environ as ENV

logoPath = ENV.logoPath



class GamePanel(wx.Panel):

    _values = ("teamPts", "oppPts", "spread", "money", "o/u")

    def __init__(self, parent, ctrl, *args, **kwargs):
        super().__init__(parent, style=wx.BORDER_SIMPLE, size=(500,60), *args, **kwargs)
        self.Bind(wx.EVT_LEFT_DCLICK, ctrl.getGameStats)

        ptsFont = wx.Font(wx.FontInfo(10).Bold())
        spreadFont = wx.Font(wx.FontInfo(12).Bold())

        self.isActive = wx.CheckBox(self, label="active", style=wx.ALIGN_RIGHT)
        self.gameDate = wx.StaticText(self, label="Jun 06", size=(40,40))
        self.gameDate.SetFont(wx.Font(wx.FontInfo(9).Bold()))
        self.logo = wx.StaticBitmap(self)
        self.values = {}

        self.values["teamPts"] = wx.StaticText(self, size=(30,40))
        self.values["teamPts"].SetFont(ptsFont)
        self.values["oppPts"] = wx.StaticText(self, size=(30,40))
        self.values["oppPts"].SetFont(ptsFont)

        self.values["spread"] = wx.StaticText(self, size=(50,40))
        self.values["spread"].SetFont(spreadFont)
        self.values["money"] = wx.StaticText(self, size=(50,40))
        self.values["money"].SetFont(spreadFont)
        self.values["o/u"] = wx.StaticText(self, size=(50,40))
        self.values["o/u"].SetFont(spreadFont)

        for item in (self.gameDate, self.logo, *self.values.values()):
            item.Bind(wx.EVT_LEFT_DCLICK, ctrl.getGameStats)


        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.isActive, 0)
        self.sizer.Add(self.gameDate, 0, wx.CENTER | wx.LEFT | wx.RIGHT, 15)
        self.sizer.Add(self.values["teamPts"], 0,  wx.CENTER)
        self.sizer.Add(self.logo, 0, wx.CENTER | wx.RIGHT, 10)
        self.sizer.Add(self.values["oppPts"], 0,  wx.CENTER | wx.RIGHT, 15)
        self.sizer.Add(self.values["spread"], 0,  wx.CENTER | wx.RIGHT, 15)
        self.sizer.Add(self.values["money"], 0,  wx.CENTER | wx.RIGHT, 15)
        self.sizer.Add(self.values["o/u"], 0, wx.CENTER | wx.RIGHT, 15)

        self.SetSizer(self.sizer)


    def setGame(self, game):
        self.SetName("{} {}".format(game["gameId"],  game["oppId"]))
        backColor = wx.WHITE if game["isHome"] == 1 else wx.Colour("KHAKI")
        self.SetBackgroundColour(backColor)

        self.isActive.SetValue(False)
        self.isActive.Hide()

        try:
            logo = wx.Image(logoPath.format(game["leagueId"], game["oppId"]), wx.BITMAP_TYPE_PNG).Scale(22, 22, wx.IMAGE_QUALITY_HIGH)
        except:
            logo = wx.Image(logoPath.format(game["leagueId"], -1), wx.BITMAP_TYPE_PNG).Scale(22, 22, wx.IMAGE_QUALITY_HIGH)

        logo = logo.ConvertToBitmap()
        self.logo.SetBitmap(logo)
        self.logo.SetName("{} {}".format(game["gameId"],  game["oppId"]))


        self.gameDate.SetLabel(game["gameDate"].strftime("%b\n%d"))
        self.gameDate.SetName("{} {}".format(game["gameId"],  game["oppId"]))

        self.values["teamPts"].SetLabel("{:3d}".format(game["teamPts"]))
        self.values["teamPts"].SetName("{} {}".format(game["gameId"],  game["oppId"]))

        self.values["oppPts"].SetLabel("{:3d}".format(game["oppPts"]))
        self.values["oppPts"].SetName("{} {}".format(game["gameId"],  game["oppId"]))

        self.values["spread"].SetLabel("{:>5}".format(str(game["spread"])))
        self.values["spread"].SetName("{} {}".format(game["gameId"],  game["oppId"]))

        try:
            self.values["money"].SetLabel("{:>5}".format(str(game["money"]) if game["money"] < 0 else "+"+str(game["money"])))
        except:
            self.values["money"].SetLabel("--")
        self.values["money"].SetName("{} {}".format(game["gameId"],  game["oppId"]))

        self.values["o/u"].SetLabel("{:>5}".format(str(game["o/u"])))
        self.values["o/u"].SetName("{} {}".format(game["gameId"],  game["oppId"]))



        moneyColor = wx.Colour("GREEN") if game["isWinner"] == 1 else wx.Colour("RED")
        spreadColor = wx.Colour("BLACK")
        ouColor = wx.Colour("BLACK")

        try:
            if game["isCover"] > 0:
                spreadColor = wx.Colour("GREEN")
            elif game["isCover"] < 0:
                spreadColor = wx.Colour("RED")
        except:
            spreadColor = wx.Colour("GREY")


        try:
            if game["isOver"] > 0:
                ouColor = wx.Colour("GREEN")
            elif game["isOver"] < 0:
                ouColor = wx.Colour("RED")
        except:
            ouColor = wx.Colour("GREY")

        self.values["spread"].SetForegroundColour(spreadColor)
        self.values["money"].SetForegroundColour(moneyColor)
        self.values["o/u"].SetForegroundColour(ouColor)





class GameLogPanel(wx.Panel):

    def __init__(self, parent, ctrl, *args, **kwargs):
        super().__init__(parent, size=(400,400), *args, **kwargs)

        self.scrollPanel = wx.ScrolledWindow(self)
        self.scrollPanel.SetScrollbars(20, 20, 50, 50)

        self.ctrl = ctrl
        self.panels = {}
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.scrollPanel.SetSizer(self.sizer)

        self.collapsePanel = wx.CollapsiblePane(self, label="edit games")
        self.collapsePanel.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.onCollapse)
        win = self.collapsePanel.GetPane()
        self.optionsPanel = OptionsPanel(win)

        self.optionsPanel.hA.Bind(wx.EVT_RADIOBOX, self.onRadio)
        self.optionsPanel.wL.Bind(wx.EVT_RADIOBOX, self.onRadio)
        self.optionsPanel.fav.Bind(wx.EVT_RADIOBOX, self.onRadio)
        self.optionsPanel.ats.Bind(wx.EVT_RADIOBOX, self.onRadio)
        self.optionsPanel.set.Bind(wx.EVT_BUTTON, self.onSet)
        self.optionsPanel.clear.Bind(wx.EVT_BUTTON, self.onClear)
        self.optionsPanel.all.Bind(wx.EVT_BUTTON, self.onAll)


        paneSz = wx.BoxSizer(wx.VERTICAL)
        paneSz.Add(self.optionsPanel, 1, wx.GROW)
        win.SetSizer(paneSz)
        paneSz.SetSizeHints(win)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.scrollPanel, 1, wx.EXPAND)
        mainSizer.Add(self.collapsePanel, 0, wx.GROW)

        self.SetSizer(mainSizer)


    def onCollapse(self, event):
        if event.GetEventObject().IsExpanded():
            for game in self.panels.values():
                game.isActive.Show()
                game.Layout()
        else:
            for game in self.panels.values():
                game.isActive.Hide()
                game.Layout()
        self.Layout()


    def onRadio(self, evt):
        hA = self.optionsPanel.hA.GetString(self.optionsPanel.hA.GetSelection())
        wL = self.optionsPanel.wL.GetString(self.optionsPanel.wL.GetSelection())
        fav = self.optionsPanel.fav.GetString(self.optionsPanel.fav.GetSelection())
        ats = self.optionsPanel.ats.GetString(self.optionsPanel.ats.GetSelection())

        for game in self.gamePool:
            # hA first
            if hA == "all":
                self.panels[game["gameId"]].isActive.SetValue(True)
            elif game["isHome"] == (hA=="home"):
                self.panels[game["gameId"]].isActive.SetValue(True)
            else:
                self.panels[game["gameId"]].isActive.SetValue(False)


            if wL == "all":
                pass
            elif game["isWinner"] and wL == "loser":

                self.panels[game["gameId"]].isActive.SetValue(False)
            elif not game["isWinner"] and wL == "winner":
                self.panels[game["gameId"]].isActive.SetValue(False)

            if fav == "all":
                pass
            elif game["money"]:
                if game["money"] < 0 and fav == "underdog":
                    self.panels[game["gameId"]].isActive.SetValue(False)
                elif game["money"] > 0 and fav == "favorite":
                    self.panels[game["gameId"]].isActive.SetValue(False)

            if ats == "all":
                pass
            elif game["isCover"] and ats == "loser":
                self.panels[game["gameId"]].isActive.SetValue(False)
            elif not game["isCover"] and ats == "cover":
                self.panels[game["gameId"]].isActive.SetValue(False)



    def onSet(self, evt):
        print("onSet")
        value = None
        if self.onOpp.isActive():
            pass
        elif self.commOpp.isActive():
            pass





    def onClear(self, evt):
        for panel in self.panels.values():
            panel.isActive.SetValue(False)


    def onAll(self, evt):
        for panel in self.panels.values():
            panel.isActive.SetValue(True)


    def setPanel(self, team):
        self.gamePool = team.getGamePool()
        self.activeIds = team.getActiveGameIds()


        self.scrollPanel.DestroyChildren()
        self.panels = {}
        for game in self.gamePool:
            newPanel = GamePanel(self.scrollPanel, self.ctrl)
            newPanel.setGame(game)
            if game["gameId"] in self.activeIds:
                newPanel.isActive.SetValue(True)
            else:
                newPanel.Hide()
            self.sizer.Add(newPanel, 1, wx.BOTTOM, 15)
            self.panels[game["gameId"]] = newPanel
