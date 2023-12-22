import datetime
import wx

from FelsonSports import Environ as ENV

from pprint import pprint

logoPath = ENV.logoPath

class ThumbPanel(wx.Panel):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, size=(120,120), style=wx.BORDER_SIMPLE, *args, **kwargs)
        self.SetBackgroundColour(wx.Colour("WHITE"))

        gdFont = wx.Font(wx.FontInfo(6))
        baseFont = wx.Font(wx.FontInfo(8))
        abrvFont = wx.Font(wx.FontInfo(11))

        self.abrvs = {}
        self.logos = {}
        self.values = {}

        self.gameDate = wx.StaticText(self, label="Today's Game")
        self.gameDate.SetFont(gdFont)

        self.gameTime = wx.StaticText(self)
        self.gameTime.SetFont(gdFont)

        self.spread = wx.StaticText(self, label="NONE")
        self.spread.SetFont(baseFont)

        self.ou = wx.StaticText(self)
        self.ou.SetFont(baseFont)

        lineSizers = {}

        for hA in ("away", "home"):
            abrv = wx.StaticText(self)
            abrv.SetFont(abrvFont)
            self.abrvs[hA] = abrv

            value = wx.StaticText(self)
            value.SetFont(baseFont)
            self.values[hA] = value

            logo = wx.StaticBitmap(self)
            self.logos[hA] = logo

            teamSizer = wx.BoxSizer()
            teamSizer.Add(logo, 1, wx.EXPAND | wx.BOTTOM, 5)
            teamSizer.Add(abrv, 1, wx.EXPAND)

            lineSizer = wx.BoxSizer()
            lineSizer.Add(teamSizer, 1, wx.EXPAND)
            lineSizer.Add(value, 0, wx.LEFT | wx.RIGHT, 8)

            lineSizers[hA] = lineSizer

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.gameDate, 0, wx.CENTER | wx.TOP, 5)
        sizer.Add(self.gameTime, 0, wx.CENTER | wx.BOTTOM, 7)
        sizer.Add(lineSizers["away"], 1, wx.EXPAND)
        sizer.Add(lineSizers["home"], 1, wx.EXPAND)
        sizer.Add(self.spread, 0, wx.CENTER | wx.TOP, 3)
        sizer.Add(self.ou, 0, wx.CENTER)

        self.SetSizer(sizer)


    def setPanel(self, game):

        gameId = game.getInfo("gameId")
        gd = game.getGamedate()
        odds = game.getOdds()

        self.SetName("{}".format(gameId))

        self.gameDate.SetName("{}".format(gameId))
        self.gameDate.SetLabel(gd.strftime("%a %b %d"))

        self.gameTime.SetName("{}".format(gameId))
        self.gameTime.SetLabel(gd.strftime("%I:%M %p"))


        self.spread.SetName("{}".format(gameId))
        self.spread.SetLabel("{}  {}".format(game.getTeam("home").getInfo("abrv"), odds.getItem(group="spread", item="homeSpread")))

        self.ou.SetName("{}".format(gameId))

        try:
            self.ou.SetLabel("{:.1f}".format(float(odds.getItem(group="total", item="total"))))
        except:
            self.ou.SetLabel("--")


        for hA in ("away", "home"):

            self.abrvs[hA].SetName("{}".format(gameId))
            self.abrvs[hA].SetLabel(game.getTeam(hA).getInfo("abrv"))

            self.logos[hA].SetName("{}".format(gameId))
            try:
                logo = wx.Image(logoPath.format(game.getInfo("leagueId"), game.getTeam(hA).getInfo("teamId")), wx.BITMAP_TYPE_PNG).Scale(22, 22, wx.IMAGE_QUALITY_HIGH)
            except:
                logo = wx.Image(logoPath.format(game.getInfo("leagueId"), -1), wx.BITMAP_TYPE_PNG).Scale(22, 22, wx.IMAGE_QUALITY_HIGH)

            logo = logo.ConvertToBitmap()
            self.logos[hA].SetBitmap(logo)

            self.values[hA].SetName("{}".format(gameId))
            try:
                self.values[hA].SetLabel("{:.0f}".format(odds.getItem(group="money", item="{}ML".format(hA))))
            except:
                self.values[hA].SetLabel("--")

        self.Layout()


    def bind(self, cmd):
        self.Bind(wx.EVT_LEFT_DCLICK, cmd)
        for item in (*self.abrvs.values(), *self.logos.values(), *self.values.values(), self.spread,
                        self.ou, self.gameDate, self.gameTime):
            item.Bind(wx.EVT_LEFT_DCLICK, cmd)


class MatchupFrame(wx.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.panels = []
        self.scrolledPanel = wx.ScrolledWindow(self, size=(850, 140))
        self.scrolledPanel.SetScrollbars(20, 20, 10, 10)
        self.scrollSizer = wx.BoxSizer()
        self.scrolledPanel.SetSizer(self.scrollSizer)

        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.scrolledPanel)
        self.SetSizer(self.sizer)


    def addPanels(self, games, bindCmd=None):
        games = sorted(games, key= lambda x: x.getInfo("gameTime"))
        for game in games:
            newPanel = ThumbPanel(self.scrolledPanel)
            newPanel.setPanel(game)
            if bindCmd:
                newPanel.bind(bindCmd)
            self.scrollSizer.Add(newPanel, 0, wx.ALL, 5)
        self.Layout()
