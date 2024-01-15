import wx

from .base_panel import BasePanel
from ..events import EVT_SOS



class SOSFrame(wx.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, size=(300,300), *args, **kwargs)
        self.Bind(EVT_SOS, self.setPanel)

        self.sosPanel = BasePanel(self)
        self.teamName = wx.StaticText(self.sosPanel, label="Team Name")

        self.oppPtsScore = wx.StaticText(self.sosPanel, label="oppPtsScore")
        self.victoryScore = wx.StaticText(self.sosPanel, label="victoryScore")
        self.homeScore = wx.StaticText(self.sosPanel, label="homeScore")
        self.awayScore = wx.StaticText(self.sosPanel, label="awayScore")
        self.homeWeight = wx.StaticText(self.sosPanel, label="homeWeight")
        self.awayWeight = wx.StaticText(self.sosPanel, label="awayWeight")

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.teamName, 0, wx.TOP | wx.BOTTOM, 10)

        lineSizer = wx.BoxSizer()
        lineSizer.Add(self.homeWeight, 1, wx.CENTER)
        lineSizer.Add(self.awayWeight, 1, wx.CENTER)
        mainSizer.Add(lineSizer, 0, wx.TOP | wx.BOTTOM | wx.EXPAND, 10)

        statSizer = wx.GridSizer(cols=2, vgap=20, hgap=20)
        statSizer.Add(self.homeScore)
        statSizer.Add(self.awayScore)
        statSizer.Add(self.oppPtsScore)
        statSizer.Add(self.victoryScore)

        mainSizer.Add(statSizer)

        self.sosPanel.SetSizer(mainSizer)


    def setPanel(self, evt):
        team = evt.GetValue()
        self.teamName.SetLabel(team.getInfo("lastName"))
        self.homeWeight.SetLabel("Home Weight: {:.2f}".format(team.sos["homeWeight"]))
        self.awayWeight.SetLabel("Away Weight: {:.2f}".format(team.sos["awayWeight"]))
        self.homeScore.SetLabel("Home Score: {:.1f}".format(team.sos["homeScore"]))
        self.awayScore.SetLabel("Away Score: {:.1f}".format(team.sos["awayScore"]))
        self.oppPtsScore.SetLabel("oppPts Score: {:.1f}".format(team.sos["oppPtsScore"]))
        self.victoryScore.SetLabel("victory Score: {:.1f}".format(team.sos["victoryScore"]))



        self.sosPanel.Layout()
