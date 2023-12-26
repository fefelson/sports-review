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

        mainSizer = wx.GridBagSizer()
        mainSizer.Add(self.title["away"], pos=(0, 3), span=(0,5), flag=wx.EXPAND)
        mainSizer.Add(wx.StaticLine(self), pos=(0, 11), span=(0,13), flag=wx.EXPAND)
        mainSizer.Add(self.title["home"], pos=(0, 28), span=(0,5))

        mainSizer.Add(self.values["away"]["win%"], pos=(2,3), flag=wx.EXPAND)
        mainSizer.Add(self.createStaticText(self, "Win %", 12, True), pos=(2,11), span=(1,2), flag=wx.EXPAND)
        mainSizer.Add(self.values["home"]["win%"], pos=(2,28), flag=wx.EXPAND)

        mainSizer.Add(self.values["away"]["winROI"], pos=(4,3))
        mainSizer.Add(self.createStaticText(self, "Win ROI%", 12, True), pos=(4,11), span=(1,2))
        mainSizer.Add(self.values["home"]["winROI"], pos=(4,28))

        mainSizer.Add(self.values["away"]["cover%"], pos=(5,3))
        mainSizer.Add(self.createStaticText(self, "Cover%", 12, True), pos=(5,11), flag=wx.EXPAND)
        mainSizer.Add(self.values["home"]["cover%"], pos=(5,28))

        mainSizer.Add(self.values["away"]["coverROI"], pos=(7,3))
        mainSizer.Add(self.createStaticText(self, "Cover ROI%", 12, True), pos=(7,11), span=(1,2), flag=wx.EXPAND)
        mainSizer.Add(self.values["home"]["coverROI"], pos=(7,28))

        mainSizer.Add(self.values["away"]["oppMed"], pos=(10,3))
        mainSizer.Add(self.createStaticText(self, "Opp Med", 12, True), pos=(10,11), span=(1,2), flag=wx.EXPAND)
        mainSizer.Add(self.values["home"]["oppMed"], pos=(10,28))

        mainSizer.Add(self.values["away"]["spreadMed"], pos=(13,3), flag=wx.EXPAND)
        mainSizer.Add(self.createStaticText(self, "Spread Med", 12, True), pos=(13,11), span=(1,2), flag=wx.EXPAND)
        mainSizer.Add(self.values["home"]["spreadMed"], pos=(13,28), flag=wx.EXPAND)

        mainSizer.Add(self.values["away"]["resultMed"], pos=(15,3), flag=wx.EXPAND)
        mainSizer.Add(self.createStaticText(self, "Result Med", 12, True), pos=(15,11), span=(1,2), flag=wx.EXPAND)
        mainSizer.Add(self.values["home"]["resultMed"], pos=(15,28), flag=wx.EXPAND)

        mainSizer.Add(gamesLabel, pos=(17,3), span=(1,4), flag=wx.EXPAND)
        mainSizer.Add(self.gameNum, pos=(17,9), flag=wx.EXPAND)


        self.SetSizer(mainSizer)
        self.Layout()



class GameOddsFrame(wx.Frame):

    def __init__(self, parent, teamIds=[], *args, **kwargs):
        super().__init__(parent, size=(550,400), *args, **kwargs)
        self.Bind(EVT_GameOdds, self.setPanel)

        self.vsPanel = VsPanel(self)

        sizer = wx.BoxSizer()
        sizer.Add(self.vsPanel)
        self.SetSizer(sizer)

        self.Layout()






    def setPanel(self, evt):
        pass
