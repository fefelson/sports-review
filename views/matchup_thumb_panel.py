import datetime
import wx

from threading import Event

from ..helpers import countResults, getRequest
from FelsonSports import Environ as ENV


logoPath = ENV.logoPath

class ThumbPanel(wx.Panel):

    def __init__(self, parent, ctrl, *args, **kwargs):
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
        self.spread.Bind(wx.EVT_LEFT_DCLICK, ctrl.onSpread)

        self.ou = wx.StaticText(self)
        self.ou.SetFont(baseFont)
        self.ou.Bind(wx.EVT_LEFT_DCLICK, ctrl.onTotal)

        lineSizers = {}

        for hA in ("away", "home"):
            abrv = wx.StaticText(self)
            abrv.SetFont(abrvFont)
            self.abrvs[hA] = abrv

            value = wx.StaticText(self)
            value.SetFont(baseFont)
            value.Bind(wx.EVT_LEFT_DCLICK, ctrl.onMoney)
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

        book = odds.getBook()

        self.SetName("{}".format(gameId))

        self.gameDate.SetName("{}".format(gameId))
        self.gameDate.SetLabel(gd.strftime("%a %b %d"))

        self.gameTime.SetName("{}".format(gameId))
        self.gameTime.SetLabel(gd.strftime("%I:%M %p"))

        try:
            spread = None
            for i in range(len(book["spread"])):
                x = book["spread"][(i+1)*-1].get("homeSpread", None)
                if x:
                    spread = x
                    break
                else:
                    x = book["spread"][(i+1)*-1].get("awaySpread", None)
                    if x:
                        spread = x
                        break
            self.spread.SetName("{}".format(gameId))
            self.spread.SetLabel("{}  {}".format(game.getTeam("home").getInfo("abrv"), spread))
        except:
            self.spread.SetName("{}".format(gameId))
            self.spread.SetLabel("{}  {}".format("--", "--"))

        self.ou.SetName("{}".format(gameId))

        try:
            oU = None
            for i in range(len(book["total"])):
                x = book["total"][(i+1)*-1].get("total", None)
                if x:
                    oU = x
                    break
            self.ou.SetLabel("{:.1f}".format(float(oU)))
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

            self.values[hA].SetName("{} {}".format(hA, gameId))
            try:
                mL = None
                for i in range(len(book["money"])):
                    x = book["money"][(i+1)*-1].get("{}ML".format(hA), None)
                    if x:
                        mL = x
                        break

                self.values[hA].SetLabel("{:.0f}".format(mL))
            except:
                self.values[hA].SetLabel("--")

        self.Layout()


    def bind(self, cmd):
        self.Bind(wx.EVT_LEFT_DCLICK, cmd)
        for item in (*self.abrvs.values(), *self.logos.values(), self.gameDate, self.gameTime):
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


    def addPanels(self, games, ctrl):
        games = sorted(games, key= lambda x: x.getInfo("gameTime"))
        for game in games:
            newPanel = ThumbPanel(self.scrolledPanel, ctrl)
            newPanel.setPanel(game)
            
            try:
                awayML = game.odds.getItem("money", "awayML")
                homeML = game.odds.getItem("money", "homeML")
                spread = game.odds.getItem("spread", "homeSpread")

                color = "WHITE"
                newEvent = Event()
                exactReq = getRequest(homeML=homeML, awayML=awayML, homeSpread=spread)
                exactReq.event = newEvent
                ctrl.league.dB.run(exactReq)
                result = countResults(exactReq.value)

                for hA in ("away", "home"):
                    if (result["gp"] >= 50 and
                        (result[hA].get("winROI", 0) >= 5 or result[hA].get("coverROI", 0) >= 5)):
                        color = "MAGENTA"

                exactMoneyReq = getRequest(homeML=homeML, awayML=awayML)
                ctrl.league.dB.run(exactMoneyReq)
                result = countResults(exactMoneyReq.value)


                for hA in ("away", "home"):
                    if (result["gp"] >= 50 and
                        (result[hA].get("winROI", 0) >= 5 or result[hA].get("coverROI", 0) >= 5)):
                        color = "SPRING GREEN"



                newPanel.SetBackgroundColour(wx.Colour(color))


            except:
                pass

            for hA in ("away", "home"):
                backColor = "WHITE"
                team = game.getTeam(hA)
                winColor, _ = team.getValueColor("teamMoneyROI", team.getOdds("teamMoneyROI"))
                atsColor, _ = team.getValueColor("cover%", team.getRecords("cover%"))
                oColor, _ = team.getValueColor("overROI", team.getOdds("overROI"))
                uColor, _ = team.getValueColor("underROI", team.getOdds("underROI"))

                if atsColor == "gold":
                    backColor = "SEA GREEN"
                elif atsColor == "red":
                    backColor = "BLACK"
                elif winColor == "gold":
                    backColor = "GOLD"
                elif winColor == "red":
                    backColor = "PURPLE"
                elif atsColor == "red":
                    backColor = "BLACK"
                elif oColor == "gold":
                    backColor = "RED"
                elif uColor == "gold":
                    backColor = "BLUE"

                newPanel.abrvs[hA].SetBackgroundColour(backColor)

            newPanel.bind(ctrl.onClick)

            self.scrollSizer.Add(newPanel, 0, wx.ALL, 5)
        self.Layout()
