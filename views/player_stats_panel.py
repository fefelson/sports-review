import wx

from .base_panel import BasePanel



class PlayerPanel(BasePanel):


    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.values = {}
        statSizer = {}

        for stat in ("gp", "start%", "mins", "fgm-fga", "fg%", "ftm-fta", "ft%", "3pm-3pa", "3p%",
                     "pts", "oreb",  "reb", "ast", "stl", "blk", "fls", "trn", "plmn"):

            if stat == "pts":
                fontSize = 15
            elif stat in ("start%", "mins"):
                fontSize = 8
            else:
                fontSize = 10

            self.values[stat] = self.createStaticText(self, label=stat, fontSize=fontSize, bold=True)
            if stat in ("gp", "start%", "mins", "pts", "plmn"):
                statSizer[stat] = self.xSizer(stat, self.values[stat])
            else:
                self.values[stat].Hide()



        self.values["fullName"] = self.createStaticText(self, label="name", fontSize=13, bold=True)
        self.values["pos"] = self.createStaticText(self, label="pos", fontSize=9, bold=True)
        self.values["inj"] = wx.Panel(self, size=(10,10))
        self.values["inj"].Hide()
        self.values["inj"].SetBackgroundColour(wx.Colour("RED"))

        nameSizer = wx.BoxSizer()
        nameSizer.Add(self.values["fullName"])
        nameSizer.Add(self.values["pos"])
        nameSizer.Add(self.values["inj"])
        nameSizer.Add(statSizer["start%"], 0, wx.LEFT, 20)

        topSizer = wx.BoxSizer()
        topSizer.Add(statSizer["pts"], 0, wx.RIGHT, 10)
        topSizer.Add(statSizer["plmn"])
        topSizer.Add(statSizer["gp"], 0, wx.LEFT, 60)
        topSizer.Add(statSizer["mins"], 0, wx.LEFT, 20)


        shotSizer = wx.BoxSizer()
        fgSizer = wx.BoxSizer()
        fgSizer.Add(self.values["fgm-fga"])
        fgSizer.Add(self.values["fg%"], 0, wx.LEFT, 10)
        shotSizer.Add(fgSizer, 0, wx.RIGHT,  10)

        ftSizer = wx.BoxSizer()
        ftSizer.Add(self.values["ftm-fta"])
        ftSizer.Add(self.values["ft%"], 0, wx.LEFT, 10)
        shotSizer.Add(ftSizer, 0, wx.RIGHT,  10)

        tpSizer = wx.BoxSizer()
        tpSizer.Add(self.values["3pm-3pa"])
        tpSizer.Add(self.values["3p%"], 0, wx.LEFT, 10)
        shotSizer.Add(tpSizer, 0, wx.RIGHT,  10)

        gridSizer = wx.BoxSizer()
        for stat in ("oreb", "reb", "ast", "stl", "blk", "trn", "fls"):
            gridSizer.Add(self.values[stat], 0, wx.LEFT, 10)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(nameSizer)
        mainSizer.Add(shotSizer)
        mainSizer.Add(topSizer, 0, wx.TOP | wx.BOTTOM, 10)
        mainSizer.Add(gridSizer)


        self.SetSizer(mainSizer)


    def setPanel(self, player):
        self.values["fullName"].SetLabel(player.getItem("fullName"))
        self.values["pos"].SetLabel(player.getItem("pos"))

        for stat in ("gp", "start%", "mins", "pts", "plmn"):

            stringForm = "{:.0f}"
            if "%" in stat:
                stringForm = "{:.1f}%"
            if stat == "plmn":
                stringForm = "{:.1f}"

            try:
                self.values[stat].SetLabel(stringForm.format(player.getItem(stat)))

                reverse = True if stat in ("trn", "fls") else False
                backColor, textColor = player.getValueColor(stat, player.getItem(stat), reverse)
                self.values[stat].SetBackgroundColour(backColor)
                self.values[stat].SetForegroundColour(textColor)
            except:
                self.values[stat].SetLabel("--")

        if (player.getValueColor("fga",player.getItem("fga"))[0] == "gold" or
            player.getValueColor("fgm", player.getItem("fgm")) == "gold"):
            self.values["fgm-fga"].Show()
            self.values["fgm-fga"].SetBackgroundColour(wx.Colour("gold"))

        if player.getValueColor("fg%",  player.getItem("fg%"))[0] == "gold":
            self.values["fg%"].Show()
            self.values["fg%"].SetBackgroundColour(wx.Colour("gold"))
        elif (player.getValueColor("fga",  player.getItem("fga"))[0] not in ("red", "pink") and
                player.getValueColor("fg%", player.getItem("fg%"))[0] == "red"):
            self.values["fg%"].Show()
            self.values["fg%"].SetBackgroundColour(wx.Colour("red"))
            self.values["fg%"].SetForegroundColour(wx.Colour("white"))

        if (player.getValueColor("fta",  player.getItem("fta"))[0] == "gold" or
            player.getValueColor("ftm",  player.getItem("ftm")) == "gold"):
            self.values["ftm-fta"].Show()
            self.values["ftm-fta"].SetBackgroundColour(wx.Colour("gold"))

        if player.getValueColor("ft%", player.getItem("ft%"))[0] == "gold":
            self.values["ft%"].Show()
            self.values["ft%"].SetBackgroundColour(wx.Colour("gold"))
        elif (player.getValueColor("fta", player.getItem("fta"))[0] not in ("red", "pink") and
                player.getValueColor("ft%", player.getItem("ft%"))[0] == "red"):
            self.values["ft%"].Show()
            self.values["ft%"].SetBackgroundColour(wx.Colour("red"))
            self.values["ft%"].SetForegroundColour(wx.Colour("white"))

        if (player.getValueColor("tpa", player.getItem("tpa"))[0] == "gold" or
            player.getValueColor("tpm", player.getItem("tpm")) == "gold"):
            self.values["3pm-3pa"].Show()
            self.values["3pm-3pa"].SetBackgroundColour(wx.Colour("gold"))

        if player.getValueColor("tp%", player.getItem("tp%"))[0] == "gold":
            self.values["3p%"].Show()
            self.values["3p%"].SetBackgroundColour(wx.Colour("gold"))
        elif (player.getValueColor("tpa", player.getItem("tpa"))[0] not in ("red", "pink") and
                player.getValueColor("tp%", player.getItem("tp%"))[0] == "red"):
            self.values["3p%"].Show()
            self.values["3p%"].SetBackgroundColour(wx.Colour("red"))
            self.values["3p%"].SetForegroundColour(wx.Colour("white"))


        for stat in ("oreb", "reb", "ast", "stl", "blk"):
            if player.getValueColor(stat, player.getItem(stat))[0] in ("gold", "green"):
                self.values[stat].Show()
                backColor, textColor = player.getValueColor(stat,  player.getItem(stat))
                self.values[stat].SetBackgroundColour(wx.Colour(backColor))
                self.values[stat].SetForegroundColour(wx.Colour(textColor))

        for stat in ("fls", "trn"):
            if player.getValueColor(stat, player.getItem(stat))[0] in ("red", "pink"):
                self.values[stat].Show()
                backColor, textColor = player.getValueColor(stat, player.getItem(stat))
                self.values[stat].SetBackgroundColour(wx.Colour(backColor))
                self.values[stat].SetForegroundColour(wx.Colour(textColor))

        self.Layout()






class PlayerStatsPanel(BasePanel):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.srolledWindow = wx.ScrolledWindow(self)
        self.srolledWindow.SetScrollbars(20, 20, 10, 10)
        self.scrollSizer = wx.GridSizer(cols=2, hgap=5, vgap=30)
        self.srolledWindow.SetSizer(self.scrollSizer)

        sizer = wx.BoxSizer()
        sizer.Add(self.srolledWindow, 1, wx.EXPAND | wx.ALL, 25)
        self.SetSizer(sizer)


    def setPanel(self, team, injuries):
        inj = [int(x) for x in injuries.keys()]
        for player in team.getPlayers():
            newPanel = PlayerPanel(self.srolledWindow)
            newPanel.setPanel(player)
            if int(player.getItem("playerId")) in inj:
                newPanel.values["inj"].Show()
            self.scrollSizer.Add(newPanel)
        self.srolledWindow.Layout()
