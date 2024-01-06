import wx

from .options_panel import OptionsPanel



logoPath = "/home/ededub/FEFelson/nba/logos/{}.png"



class GamePanel(wx.Panel):

    _values = ("teamPts", "oppPts", "spread", "money", "o/u")

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, style=wx.BORDER_SIMPLE, size=(500,60), *args, **kwargs)

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


    def bind(self, cmd):
        self.Bind(wx.EVT_LEFT_DCLICK, cmd)
        for item in (self.gameDate, self.logo, *self.values.values()):
            item.Bind(wx.EVT_LEFT_DCLICK, cmd)


    def setGame(self, game):
        self.SetName("{} {}".format(game["gameId"],  game["oppId"]))
        backColor = wx.WHITE if game["isHome"] == 1 else wx.Colour("KHAKI")
        self.SetBackgroundColour(backColor)

        self.isActive.SetValue(False)
        self.isActive.Hide()

        logo = wx.Image(logoPath.format(game["oppId"]), wx.BITMAP_TYPE_ANY).Scale(40, 40, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
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

        self.values["money"].SetLabel("{:>5}".format(str(game["money"]) if game["money"] < 0 else "+"+str(game["money"])))
        self.values["money"].SetName("{} {}".format(game["gameId"],  game["oppId"]))

        self.values["o/u"].SetLabel("{:>5}".format(str(game["o/u"])))
        self.values["o/u"].SetName("{} {}".format(game["gameId"],  game["oppId"]))



        moneyColor = wx.Colour("GREEN") if game["isWinner"] == 1 else wx.Colour("RED")
        spreadColor = wx.Colour("BLACK")
        ouColor = wx.Colour("BLACK")

        if game["isCover"] > 0:
            spreadColor = wx.Colour("GREEN")
        elif game["isCover"] < 0:
            spreadColor = wx.Colour("RED")

        if game["isOver"] > 0:
            ouColor = wx.Colour("GREEN")
        elif game["isOver"] < 0:
            ouColor = wx.Colour("RED")

        self.values["spread"].SetForegroundColour(spreadColor)
        self.values["money"].SetForegroundColour(moneyColor)
        self.values["o/u"].SetForegroundColour(ouColor)





class GameLogPanel(wx.Panel):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, size=(400,400), *args, **kwargs)

        self.scrollPanel = wx.ScrolledWindow(self)
        self.scrollPanel.SetScrollbars(20, 20, 50, 50)
        self.panels = {}
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.scrollPanel.SetSizer(self.sizer)

        self.collapsePanel = wx.CollapsiblePane(self, label="edit games")
        win = self.collapsePanel.GetPane()
        self.optionsPanel = OptionsPanel(win)
        paneSz = wx.BoxSizer(wx.VERTICAL)
        paneSz.Add(self.optionsPanel, 1, wx.GROW)
        win.SetSizer(paneSz)
        paneSz.SetSizeHints(win)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.scrollPanel, 1, wx.EXPAND)
        mainSizer.Add(self.collapsePanel, 0, wx.GROW)

        self.SetSizer(mainSizer)

    def addGame(self, game, bindCmd):
        self.listPanel.addGame(game, bindCmd)




    def setPanel(self, gamePool, activeIds, bndCmd):
        self.scrollPanel.DestroyChildren()
        self.panels = {}
        for game in gamePool:
            newPanel = GamePanel(self.scrollPanel)
            newPanel.setGame(game)
            if game["gameId"] in activeIds:
                newPanel.isActive.SetValue(True)
            else:
                newPanel.Hide()
            newPanel.bind(bndCmd)
            self.sizer.Add(newPanel, 1, wx.BOTTOM, 15)
            self.panels[game["gameId"]] = newPanel
