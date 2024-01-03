import wx

from .base_panel import BasePanel
from ..events import EVT_GameOdds


class VsPanel(BasePanel):

    def __init__(self, parent, teamIds=[], *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.title = {}
        self.values = {"away":{}, "home":{}}




        for hA in ("away", "home"):
            self.title[hA] = wx.StaticText(self, label="{} {}".format(hA.upper(), "N"))
            for key in ("win%", "winROI", "cover%", "coverROI", "oppMed", "spreadMed",
                        "resultMed"):
                self.values[hA][key] = wx.StaticText(self, label=key)

        gamesLabel = wx.StaticText(self, label="Games in Set:")
        self.gameNum = wx.StaticText(self)

        mainSizer = wx.GridSizer(cols=3,vgap=5, hgap=5)
        mainSizer.Add(self.title["away"])
        mainSizer.Add(wx.StaticLine(self))
        mainSizer.Add(self.title["home"])

        mainSizer.Add(self.values["away"]["win%"])
        mainSizer.Add(self.createStaticText(self, "Win %", 12, True))
        mainSizer.Add(self.values["home"]["win%"])

        mainSizer.Add(self.values["away"]["winROI"])
        mainSizer.Add(self.createStaticText(self, "Win ROI%", 12, True))
        mainSizer.Add(self.values["home"]["winROI"])

        mainSizer.Add(self.values["away"]["cover%"])
        mainSizer.Add(self.createStaticText(self, "Cover%", 12, True))
        mainSizer.Add(self.values["home"]["cover%"])

        mainSizer.Add(self.values["away"]["coverROI"])
        mainSizer.Add(self.createStaticText(self, "Cover ROI%", 12, True))
        mainSizer.Add(self.values["home"]["coverROI"])

        mainSizer.Add(self.values["away"]["oppMed"])
        mainSizer.Add(self.createStaticText(self, "Opp Med", 12, True))
        mainSizer.Add(self.values["home"]["oppMed"])

        mainSizer.Add(self.values["away"]["spreadMed"])
        mainSizer.Add(self.createStaticText(self, "Spread Med", 12, True))
        mainSizer.Add(self.values["home"]["spreadMed"])

        mainSizer.Add(self.values["away"]["resultMed"])
        mainSizer.Add(self.createStaticText(self, "Result Med", 12, True))
        mainSizer.Add(self.values["home"]["resultMed"])

        mainSizer.Add(gamesLabel)
        mainSizer.Add(self.gameNum)


        self.SetSizer(mainSizer)
        self.Layout()



class GameOddsFrame(wx.Frame):

    def __init__(self, parent, teamIds=[], *args, **kwargs):
        super().__init__(parent, size=(550,400), *args, **kwargs)
        self.Bind(EVT_GameOdds, self.setPanel)

        self.vsPanel = VsPanel(self)

        sizer = wx.BoxSizer()
        sizer.Add(self.vsPanel, 0, wx.ALL, 10)
        self.SetSizer(sizer)

        self.Layout()


    def setPanel(self, evt):
        info = evt.GetValue()
        print(info)

        for hA in ("away", "home"):
            self.vsPanel.title[hA].SetLabel("{} {}".format(hA, info[hA]["ML"]))
            self.vsPanel.values[hA]["win%"].SetLabel("{:.0f}%".format(info[hA]["win%"]))
            self.vsPanel.values[hA]["cover%"].SetLabel("{:.0f}%".format(info[hA]["cover%"]))
            self.vsPanel.values[hA]["winROI"].SetLabel("{:.0f}%".format(info[hA]["winROI"]))
            self.vsPanel.values[hA]["coverROI"].SetLabel("{:.0f}%".format(info[hA]["coverROI"]))
