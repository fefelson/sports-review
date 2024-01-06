import wx

from .base_panel import BasePanel
from ..events import EVT_Possessions



class PossesionsFrame(wx.Frame):

    _possDict = {"title": None,
                 "total": None,
                 "total%": None,
                 "win%":None,
                 "cover%":None,
                 "over%": None
                 }

    def __init__(self, parent, ctrl, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.Bind(EVT_Possessions, self.setPanel)

        self.possessPanel = BasePanel(self)
        self.teamName = wx.StaticText(self.possessPanel, label="Team Name")
        self.mean = wx.StaticText(self.possessPanel, label="mean")
        self.median = wx.StaticText(self.possessPanel, label="median")
        self.mode = wx.StaticText(self.possessPanel, label="mode")
        self.std = wx.StaticText(self.possessPanel, label="std")

        self.possBoxes = []
        possSizers = []
        for i in range(5):
            newPoss = self._possDict.copy()
            newPoss["title"] = wx.StaticText(self.possessPanel, label="possRange {}".format(i))
            newPoss["total"] = wx.StaticText(self.possessPanel, label="total")
            newPoss["total%"] = wx.StaticText(self.possessPanel, label="total%")
            newPoss["win%"] = wx.StaticText(self.possessPanel, label="win%")
            newPoss["cover%"] = wx.StaticText(self.possessPanel, label="cover%")
            newPoss["over%"] = wx.StaticText(self.possessPanel, label="over%")
            newPoss["spread"] = wx.StaticText(self.possessPanel, label="spread")
            newPoss["o/u"] = wx.StaticText(self.possessPanel, label="o/u")
            self.possBoxes.append(newPoss)

            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(newPoss["title"], 0, wx.TOP | wx.BOTTOM | wx.CENTER, 5)
            sizer.Add(newPoss["total"], 0, wx.TOP | wx.BOTTOM | wx.CENTER, 5)
            sizer.Add(newPoss["total%"], 0, wx.TOP | wx.BOTTOM | wx.CENTER, 5)
            sizer.Add(newPoss["win%"], 0, wx.TOP | wx.BOTTOM | wx.CENTER, 5)
            sizer.Add(newPoss["cover%"], 0, wx.TOP | wx.BOTTOM | wx.CENTER, 5)
            sizer.Add(newPoss["over%"], 0, wx.TOP | wx.BOTTOM | wx.CENTER, 5)
            sizer.Add(newPoss["spread"], 0, wx.TOP | wx.BOTTOM | wx.CENTER, 5)
            sizer.Add(newPoss["o/u"], 0, wx.TOP | wx.BOTTOM | wx.CENTER, 5)
            possSizers.append(sizer)



        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.teamName, 0, wx.TOP | wx.BOTTOM, 10)

        statsSizer = wx.BoxSizer()
        statsSizer.Add(self.mean, 0, wx.LEFT | wx.RIGHT, 5)
        statsSizer.Add(self.median, 0, wx.LEFT | wx.RIGHT, 5)
        statsSizer.Add(self.mode, 0, wx.LEFT | wx.RIGHT, 5)
        statsSizer.Add(self.std, 0, wx.LEFT | wx.RIGHT, 5)

        mainSizer.Add(statsSizer)

        gridSizer = wx.GridSizer(cols=5, hgap=15, vgap=5)
        for sizer in possSizers:
            gridSizer.Add(sizer)
        mainSizer.Add(gridSizer, 1, wx.TOP, 20)
        self.possessPanel.SetSizer(mainSizer)

        self.Layout()


    def setPanel(self, evt):
        team = evt.GetValue()
        poss = team.getPossessions()
        totalGames = sum([p["gp"] for p in poss["boxes"]])
        print(totalGames)
        self.teamName.SetLabel(team.getInfo("abrv"))
        self.mean.SetLabel("mean: {:.1f}".format(poss["mean"]))
        self.median.SetLabel("median: {:.1f}".format(poss["median"]))
        self.mode.SetLabel("mode: {:.1f}".format(poss["mode"]))
        self.std.SetLabel("std: {:.1f}".format(poss["std"]))

        for i, box in enumerate(poss["boxes"]):
            possBox = self.possBoxes[i]
            possBox["title"].SetLabel(box["title"])
            possBox["total"].SetLabel("gp: {}".format(box["gp"]))
            possBox["total%"].SetLabel("gp%: {:.0f}%".format(box["gp"]/totalGames*100))
            if box["gp"]:
                possBox["win%"].SetLabel("win%: {:.0f}%".format(box["win%"]))
                possBox["cover%"].SetLabel("cover%: {:.0f}%".format(box["spread%"]))
                possBox["over%"].SetLabel("over%: {:.0f}%".format(box["over%"]))
                possBox["spread"].SetLabel("spread: {:.1f}".format(box["spread"]))
                possBox["o/u"].SetLabel("o/u: {:.1f}".format(box["o/u"]))


        self.possessPanel.Layout()
