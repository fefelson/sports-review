import wx
from .base_panel import BasePanel
from ..events import EVT_GameStats


class BasketballStatsPanel(BasePanel):

    _teamStats = ("pts", "fga", "fgm", "fg%", "fta", "ftm", "ft%", "tpa", "tpm", "tp%", "tov%", "oreb%", "dreb%", )

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.Bind(EVT_GameStats, self.setPanel)

        self.values = {"offense": {}, "defense":{}}
        self._Layout()


    def _Layout(self):

        self.values["offense"]["name"] = self.createStaticText(self, "Team", 15, True)
        self.values["defense"]["name"] = self.createStaticText(self, "Opp", 12, False)

        for offDef in ("offense", "defense"):
            for abrv in self._teamStats:
                self.values[offDef][abrv] = self.createStaticText(self, abrv, 10, True)


        mainSizer = wx.GridBagSizer()
        mainSizer.Add(self.values["defense"]["name"], pos=(0, 3), span=(0,5), flag=wx.EXPAND)
        mainSizer.Add(wx.StaticLine(self), pos=(0, 11), span=(0,13), flag=wx.EXPAND)
        mainSizer.Add(self.values["offense"]["name"], pos=(0, 28), span=(0,5))

        mainSizer.Add(self.values["defense"]["pts"], pos=(2,3), span=(0,5), flag=wx.EXPAND)
        mainSizer.Add(self.createStaticText(self, "Points", 12, True), pos=(2,11), span=(0,13), flag=wx.EXPAND)
        mainSizer.Add(self.values["offense"]["pts"], pos=(2,28), span=(0,5), flag=wx.EXPAND)

        mainSizer.Add(self.xSizer("fgm", self.values["defense"]["fgm"]), pos=(4,2), span=(2,1))
        mainSizer.Add(wx.StaticText(self, label="-"), pos=(5,3))
        mainSizer.Add(self.xSizer("fga", self.values["defense"]["fga"]), pos=(4,4), span=(2,1))
        mainSizer.Add(self.values["defense"]["fg%"], pos=(5,6))
        mainSizer.Add(self.createStaticText(self, "Field Goals", 12, True), pos=(4,11), span=(2,13), flag=wx.EXPAND)
        mainSizer.Add(self.xSizer("fgm", self.values["offense"]["fgm"]), pos=(4,27), span=(2,1))
        mainSizer.Add(wx.StaticText(self, label="-"), pos=(5,28))
        mainSizer.Add(self.xSizer("fga", self.values["offense"]["fga"]), pos=(4,29), span=(2,1))
        mainSizer.Add(self.values["offense"]["fg%"], pos=(5,31))

        mainSizer.Add(self.xSizer("ftm", self.values["defense"]["ftm"]), pos=(7,2), span=(2,1))
        mainSizer.Add(wx.StaticText(self, label="-"), pos=(8,3))
        mainSizer.Add(self.xSizer("fta", self.values["defense"]["fta"]), pos=(7,4), span=(2,1))
        mainSizer.Add(self.values["defense"]["ft%"], pos=(8,6))
        mainSizer.Add(self.createStaticText(self, "Free Throws", 12, True), pos=(7,11), span=(2,13), flag=wx.EXPAND)
        mainSizer.Add(self.xSizer("ftm", self.values["offense"]["ftm"]), pos=(7,27), span=(2,1))
        mainSizer.Add(wx.StaticText(self, label="-"), pos=(8,28))
        mainSizer.Add(self.xSizer("fta", self.values["offense"]["fta"]), pos=(7,29), span=(2,1))
        mainSizer.Add(self.values["offense"]["ft%"], pos=(8,31))

        mainSizer.Add(self.xSizer("tpm", self.values["defense"]["tpm"]), pos=(10,2), span=(2,1))
        mainSizer.Add(wx.StaticText(self, label="-"), pos=(11,3))
        mainSizer.Add(self.xSizer("tpa", self.values["defense"]["tpa"]), pos=(10,4), span=(2,1))
        mainSizer.Add(self.values["defense"]["tp%"], pos=(11,6))
        mainSizer.Add(self.createStaticText(self, "Three Points", 12, True), pos=(10,11), span=(2,13), flag=wx.EXPAND)
        mainSizer.Add(self.xSizer("tpm", self.values["offense"]["tpm"]), pos=(10,27), span=(2,1))
        mainSizer.Add(wx.StaticText(self, label="-"), pos=(11,28))
        mainSizer.Add(self.xSizer("tpa", self.values["offense"]["tpa"]), pos=(10,29), span=(2,1))
        mainSizer.Add(self.values["offense"]["tp%"], pos=(11,31))

        mainSizer.Add(self.values["defense"]["tov%"], pos=(13,3), span=(0,5), flag=wx.EXPAND)
        mainSizer.Add(self.createStaticText(self, "Turnovers", 12, True), pos=(13,11), span=(0,13), flag=wx.EXPAND)
        mainSizer.Add(self.values["offense"]["tov%"], pos=(13,28), span=(0,5), flag=wx.EXPAND)

        mainSizer.Add(self.xSizer("oreb", self.values["defense"]["oreb%"]), pos=(15,3), span=(2,1), flag=wx.EXPAND)
        mainSizer.Add(self.xSizer("dreb", self.values["defense"]["dreb%"]), pos=(15,7), span=(2,1), flag=wx.EXPAND)
        mainSizer.Add(self.createStaticText(self, "Rebounds", 12, True), pos=(15,11), span=(2,13), flag=wx.EXPAND)
        mainSizer.Add(self.xSizer("oreb", self.values["offense"]["oreb%"]), pos=(15,28), span=(2,1), flag=wx.EXPAND)
        mainSizer.Add(self.xSizer("dreb", self.values["offense"]["dreb%"]), pos=(15,32), span=(2,1), flag=wx.EXPAND)

        self.SetSizer(mainSizer)


    def setPanel(self, evt):
        teamStats = evt.GetValue()
        for offDef in ("offense", "defense"):
            for key in ("name", "pts", "fga", "fgm", "fg%", "fta", "ftm", "ft%", "tpa", "tpm", "tp%",
                        "oreb%", "dreb%", "tov%"):
                if key == "name":
                    try:
                        self.values[offDef]["name"].SetLabel(teamStats.getValue("{}_{}".format(offDef, key)))
                    except:
                        pass
                else:
                    try:
                        if "%" in key:
                            strForm = "{:.0f}%"
                        else:
                            strForm = "{:.0f}"
                        self.values[offDef][key].SetLabel(strForm.format(teamStats.getValue("{}_{}".format(offDef, key))))
                    except AssertionError:
                        self.values[offDef][key].SetLabel("--")
        self.Layout()
