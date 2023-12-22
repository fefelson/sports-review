import wx

from .base_panel import BasePanel
from .matchup_thumb_panel import ThumbPanel
from ..helpers import adjust_readability, hex_to_rgb


imagePath = "/home/ededub/FEFelson/{}/logos/{}.png"

class TitlePanel(BasePanel):

    def __init__(self, parent, hA="home", *args, **kwargs):
        super().__init__(parent, size=(700,-1), *args, **kwargs)


        self.sos = {}
        self.money = {}

        self.overallPanel = BasePanel(self, size=(180,160), style=wx.BORDER_SIMPLE)
        self.matchupPanel = ThumbPanel(self)
        self.matchupPanel.SetSize((180,160))

        overallLabel = self.createStaticText(self.overallPanel, label="Overall", fontSize=12, bold=True)
        sosLabel = self.createStaticText(self.overallPanel, label="SOS", fontSize=12, bold=True)


        self.sos["score"] = self.createStaticText(self.overallPanel, label="00", fontSize=28, bold=True)
        self.sos["SOS"] = self.createStaticText(self.overallPanel, label="00", fontSize=20, bold=True)
        self.sos["offEff"] = self.createStaticText(self.overallPanel, label="000", fontSize=12, bold=True)
        self.sos["defEff"] = self.createStaticText(self.overallPanel, label="000", fontSize=12, bold=True)
        self.sos["poss"] = self.createStaticText(self.overallPanel, label="000", fontSize=12, bold=True)

        self.logo = wx.StaticBitmap(self)

        self.firstName = self.createStaticText(self, label="First", fontSize=18, bold=True)
        self.firstName.SetMaxSize(wx.Size(200,-1))
        self.lastName = self.createStaticText(self, label="Last", fontSize=20, bold=True)
        self.lastName.SetMaxSize(wx.Size(200,-1))



        gamesLabel = self.createStaticText(self, label="gp", fontSize=18, bold=True)
        self.games = self.createStaticText(self, label="0", fontSize=18, bold=True)

        winPctLabel = self.createStaticText(self, label="WIN Pct:", fontSize=12, bold=False)
        winROILabel = self.createStaticText(self, label="roi:", fontSize=12, bold=False)
        atsPctLabel = self.createStaticText(self, label="ATS Pct:", fontSize=12, bold=False)
        atsROILabel = self.createStaticText(self, label="roi:", fontSize=12, bold=False)
        self.ouLabel = self.createStaticText(self, label="O/U Pct:", fontSize=12, bold=False)
        ouROILabel = self.createStaticText(self, label="roi:", fontSize=12, bold=False)


        self.money["win%"] = self.createStaticText(self, label="0%", fontSize=12, bold=True)
        self.money["teamMoneyROI"] = self.createStaticText(self, label="0%", fontSize=12, bold=True)
        self.money["cover%"] = self.createStaticText(self, label="0%", fontSize=12, bold=True)
        self.money["teamSpreadROI"] = self.createStaticText(self, label="0%", fontSize=12, bold=True)
        self.money["ou%"] = self.createStaticText(self, label="0%", fontSize=12, bold=True)
        self.money["ouROI"] = self.createStaticText(self, label="0%", fontSize=12, bold=True)


        offDefSizer = wx.BoxSizer()
        offenseSizer = self.overallPanel.xSizer("off", self.sos["offEff"])
        defenseSizer = self.overallPanel.xSizer("def", self.sos["defEff"])
        weightSizer = self.overallPanel.xSizer("poss", self.sos["poss"])


        offDefSizer.Add(offenseSizer, 1)
        offDefSizer.Add(weightSizer, 1)
        offDefSizer.Add(defenseSizer, 1)


        overallSizer = wx.BoxSizer(wx.VERTICAL)
        overallSizer.Add(overallLabel, 0, wx.CENTER)
        overallSizer.Add(self.sos["score"], 0, wx.CENTER)
        overallSizer.Add(sosLabel, 0, wx.CENTER)
        overallSizer.Add(self.sos["SOS"], 0, wx.CENTER)
        overallSizer.Add(offDefSizer, 0, wx.EXPAND)


        self.overallPanel.SetSizer(overallSizer)


        mainSizer = wx.BoxSizer()
        outSideSizer = wx.BoxSizer(wx.VERTICAL)
        outSideSizer.Add(self.logo, 0, wx.CENTER)
        outSideSizer.Add(gamesLabel, 0, wx.CENTER)
        outSideSizer.Add(self.games, 0, wx.CENTER)

        moneySizer = wx.GridBagSizer()
        moneySizer.Add(winPctLabel, pos=(0,0), span=(1,2))
        moneySizer.Add(self.money["win%"], pos=(0,3))
        moneySizer.Add(winROILabel, pos=(0,6))
        moneySizer.Add(self.money["teamMoneyROI"], pos=(0,8))
        moneySizer.Add(atsPctLabel, pos=(1,0), span=(1,2))
        moneySizer.Add(self.money["cover%"], pos=(1,3))
        moneySizer.Add(atsROILabel, pos=(1,6))
        moneySizer.Add(self.money["teamSpreadROI"], pos=(1,8))
        moneySizer.Add(self.ouLabel, pos=(3,0), span=(1,2))
        moneySizer.Add(self.money["ou%"], pos=(3,3))
        moneySizer.Add(ouROILabel, pos=(3,6))
        moneySizer.Add(self.money["ouROI"], pos=(3,8))

        middleSizer = wx.BoxSizer(wx.VERTICAL)
        middleSizer.Add(self.firstName, 0, wx.CENTER)
        middleSizer.Add(self.lastName, 0, wx.CENTER)
        middleSizer.Add(moneySizer, 1, wx.EXPAND | wx.ALL, 20)

        if hA == "home":
            mainSizer.Add(self.overallPanel, 0, wx.EXPAND)
            mainSizer.Add(middleSizer, 1, wx.LEFT | wx.RIGHT, 5)
            mainSizer.Add(outSideSizer, 0, wx.EXPAND)
            mainSizer.Add(self.matchupPanel, 0, wx.EXPAND)

        else:
            mainSizer.Add(self.matchupPanel, 0, wx.EXPAND)
            mainSizer.Add(outSideSizer, 0, wx.EXPAND)
            mainSizer.Add(middleSizer, 1, wx.LEFT | wx.RIGHT, 5)
            mainSizer.Add(self.overallPanel, 0, wx.EXPAND)

        self.SetSizer(mainSizer)


    def setPanel(self, team):

        try:
            primaryColor, secondColor = team.getColors()
            backColor, textColor = adjust_readability(hex_to_rgb(secondColor), hex_to_rgb(primaryColor))
        except:
            backColor = (240, 240, 230)
            textColor = (30, 30, 30)
        self.SetBackgroundColour(wx.Colour(backColor))
        self.SetForegroundColour(wx.Colour(textColor))

        self.overallPanel.SetBackgroundColour(wx.Colour(textColor))
        self.overallPanel.SetForegroundColour(wx.Colour(backColor))

        self.firstName.SetLabel(team.getInfo("firstName"))
        self.firstName.SetName("{} {}".format("name", team.getInfo("teamId")))

        self.lastName.SetLabel(team.getInfo("lastName"))
        self.lastName.SetName("{} {}".format("name", team.getInfo("teamId")))

        try:
            logo = wx.Image(imagePath.format(team.getInfo("leagueId"), team.getInfo("teamId")), wx.BITMAP_TYPE_ANY).Scale(125, 125, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        except:
            logo = wx.Image(imagePath.format(team.getInfo("leagueId"), -1), wx.BITMAP_TYPE_PNG).Scale(125, 125, wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()

        self.logo.SetBitmap(logo)
        self.logo.SetName("{} {}".format("name", team.getInfo("teamId")))

        try:
            self.games.SetLabel("{:2d}".format(team.getStats("gp")))
        except:
            self.games.SetLabel("--")
        self.games.SetName("{} {}".format("gp", team.getInfo("teamId")))


        for key in ("score", "poss", "offEff", "defEff"):
            stringForm = "{:3.2f}" if key == "score" else "{:3.0f}"
            reverse = True if key == "defEff" else False

            self.sos[key].SetLabel(stringForm.format(team.getStats(key)))
            backColor, textColor = team.getValueColor(key, team.getStats(key), reverse)
            self.sos[key].SetBackgroundColour(backColor)
            self.sos[key].SetForegroundColour(textColor)

            self.sos[key].SetName("{} {}".format(key, team.getInfo("teamId")))

        self.sos["SOS"].SetLabel("{:3.0f}".format(team.getSOS("SOS")))
        # backColor, textColor = team.getValueColor(key, team.getSOS("SOS"), reverse)
        self.sos["SOS"].SetBackgroundColour("grey")
        self.sos["SOS"].SetForegroundColour("white")
        self.sos["SOS"].SetName("{} {}".format("SOS", team.getInfo("teamId")))


        try:
            overPct = team.getRecords("over%")
            if overPct > 50:
                self.ouLabel.SetLabel("OVER Pct: ")
                self.money["ou%"].SetLabel("{:3.1f}%".format(overPct))
                backColor, textColor = team.getValueColor("over%", overPct)
                self.money["ou%"].SetBackgroundColour(backColor)
                self.money["ou%"].SetForegroundColour(textColor)


                self.money["ouROI"].SetLabel("{:3.1f}%".format(team.getOdds("overROI")))
                backColor, textColor = team.getValueColor("overROI", team.getOdds("overROI"))
                self.money["ouROI"].SetBackgroundColour(backColor)
                self.money["ouROI"].SetForegroundColour(textColor)

            elif overPct < 50:
                self.ouLabel.SetLabel("UNDER Pct: ")
                self.money["ou%"].SetLabel("{:3.1f}%".format(100-overPct))
                backColor, textColor = team.getValueColor("under%", 100-overPct)
                self.money["ou%"].SetBackgroundColour(backColor)
                self.money["ou%"].SetForegroundColour(textColor)


                self.money["ouROI"].SetLabel("{:3.1f}%".format(team.getOdds("underROI")))
                backColor, textColor = team.getValueColor("underROI", team.getOdds("underROI"))
                self.money["ouROI"].SetBackgroundColour(backColor)
                self.money["ouROI"].SetForegroundColour(textColor)

            else:
                self.ouLabel.SetLabel("O/U Pct: ")
                self.money["ou%"].SetLabel("--")
                self.money["ou%"].SetBackgroundColour("grey")
                self.money["ou%"].SetForegroundColour("white")

                self.money["ouROI"].SetLabel("{:3.1f}%".format(team.getOdds("underROI")))
                backColor, textColor = team.getValueColor("underROI", team.getOdds("underROI"))
                self.money["ouROI"].SetBackgroundColour(backColor)
                self.money["ouROI"].SetForegroundColour(textColor)

        except:
            self.ouLabel.SetLabel("O/U Pct: ")
            self.money["ou%"].SetLabel("--")
            self.money["ou%"].SetBackgroundColour("grey")
            self.money["ou%"].SetForegroundColour("white")

            self.money["ouROI"].SetLabel("--")
            self.money["ouROI"].SetBackgroundColour("grey")
            self.money["ouROI"].SetForegroundColour("white")

        self.money["ou%"].SetName("{} {}".format("o/u", team.getInfo("teamId")))
        self.money["ouROI"].SetName("{} {}".format("ouROI", team.getInfo("teamId")))


        for key in ("win%", "cover%"):
            try:
                self.money[key].SetLabel("{:2.0f}%".format(team.getRecords(key)))
                backColor, textColor = team.getValueColor(key, team.getRecords(key))
                self.money[key].SetBackgroundColour(backColor)
                self.money[key].SetForegroundColour(textColor)

            except:
                self.money[key].SetLabel("--")
                self.money[key].SetBackgroundColour("grey")
                self.money[key].SetForegroundColour("white")
            self.money[key].SetName("{} {}".format(key, team.getInfo("teamId")))


        for key in ("teamMoneyROI", "teamSpreadROI"):
            try:
                self.money[key].SetLabel("{:3.1f}%".format(team.getOdds(key)))
                backColor, textColor = team.getValueColor(key, team.getOdds(key))
                self.money[key].SetBackgroundColour(backColor)
                self.money[key].SetForegroundColour(textColor)

            except:
                self.money[key].SetLabel("--")
                self.money[key].SetBackgroundColour("grey")
                self.money[key].SetForegroundColour("white")
            self.money[key].SetName("{} {}".format(key, team.getInfo("teamId")))


    def bind(self, bindCmd):
        for item in (self.firstName, self.lastName, self.logo, self.games):
            item.Bind(wx.EVT_LEFT_DCLICK, bindCmd)

        for key in self.money.keys():
            self.money[key].Bind(wx.EVT_LEFT_DCLICK, bindCmd)

        for key in self.sos.keys():
            self.sos[key].Bind(wx.EVT_LEFT_DCLICK, bindCmd)
