class BballPlayerStatsPanel(wx.ScrolledWindow):

    _statList = ("gp", "start%", "fg%", "ft%", "tp%", "pts", "oreb",  "reb",
                    "ast", "stl", "blk", "trn", "fls", "mins", "plmn")

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, size=((150,500)), *args, **kwargs)
        self.SetScrollbars(20, 20, 50, 50)

        mainSizer = wx.BoxSizer()
        self.values = []

        teamSizer = wx.BoxSizer(wx.VERTICAL)

        for i in range(10):
            items = {}
            self.values.append({})

            for stat in self._statList:
                if stat in ("tpa","tp%"):
                    label = self.makeLabel("3"+stat[1:])
                else:
                    label = self.makeLabel(stat)
                if stat != "pts":
                    font = wx.Font(wx.FontInfo(10).Bold())
                elif stat in ("start%", "mins", "plmn"):
                    font = wx.Font(wx.FontInfo(8).Bold())

                else:
                    font = wx.Font(wx.FontInfo(15).Bold())

                text = wx.StaticText(self)
                text.SetFont(font)

                self.values[i][stat] = text
                items[stat] = self.xSizer(label, text)

            statSizer = wx.BoxSizer()
            recSizer = wx.BoxSizer(wx.VERTICAL)

            row1 = wx.BoxSizer()
            row1.Add(items["fg%"], 0, wx.RIGHT, 35)
            row1.Add(items["ft%"], 0, wx.RIGHT, 35)
            row1.Add(items["tp%"])


            recSizer.Add(row1, 0, wx.BOTTOM, 10)

            row2 = wx.BoxSizer()
            row2.Add(items["reb"], 0, wx.RIGHT, 10)
            row2.Add(items["oreb"], 0, wx.RIGHT, 35)
            row2.Add(items["ast"], 0, wx.RIGHT, 10)
            row2.Add(items["stl"], 0, wx.RIGHT, 10)
            row2.Add(items["blk"], 0, wx.RIGHT, 30)
            row2.Add(items["trn"], 0, wx.RIGHT, 10)
            row2.Add(items["fls"], 0, wx.RIGHT, 10)

            recSizer.Add(row2, 0, wx.BOTTOM, 10)

            statSizer.Add(items["pts"], 0, wx.CENTER | wx.RIGHT, 35)
            statSizer.Add(recSizer, 0)


            sizer = wx.BoxSizer(wx.VERTICAL)

            name = wx.StaticText(self)
            name.SetFont(wx.Font(wx.FontInfo(13).Bold()))

            pos = wx.StaticText(self)
            pos.SetFont(wx.Font(wx.FontInfo(9)))

            self.values[i]["name"] = name
            self.values[i]["pos"] = pos
            self.values[i]["inj"] = wx.Panel(self, size=(10,10))


            nameSizer = wx.BoxSizer()
            nameSizer.Add(name, 1, wx.EXPAND | wx.RIGHT, 15)
            nameSizer.Add(pos, 0, wx.EXPAND | wx.RIGHT, 5)
            nameSizer.Add(self.values[i]["inj"], 0, wx.CENTER | wx.RIGHT, 15)
            nameSizer.Add(items["gp"], 0, wx.RIGHT, 10)
            nameSizer.Add(items["start%"], 0, wx.RIGHT, 10)
            nameSizer.Add(items["mins"], 0, wx.RIGHT, 10)
            nameSizer.Add(items["plmn"], 0, wx.RIGHT, 10)

            sizer.Add(nameSizer, 0, wx.BOTTOM, 25)
            sizer.Add(statSizer)
            teamSizer.Add(sizer, 1, wx.BOTTOM, 10)
            teamSizer.Add(wx.StaticLine(self), 0, wx.EXPAND)

        self.SetSizer(teamSizer)


    def setPlayer(self, i, player):

        for key in ("name", "pos", "gp","start%","fg%", "ft%", "tp%", "pts", "oreb",  "reb",
                    "ast", "stl", "blk", "trn", "fls", "mins", "plmn"):
            try:
                if key in ("fg%", "ft%", "tp%", "start%"):
                    text = "{:.0f}%".format(player[key]*100)
                elif key in ("name", "pos"):
                    if player[key]:
                        text = player[key]
                    else:
                        text = "n/a"
                elif key in ("pts", "trn", "fls", "plmn",):
                    text = "{:.1f}".format(player[key])
                else:
                    text = "{:.0f}".format(player[key])
            except:
                text = "--"

            self.values[i][key].SetLabel(text)
