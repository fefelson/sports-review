import wx

from .gamelog_panel import GameLogPanel
from .player_stats_panel import PlayerStatsPanel
from .tags_panel import TagPanel
from .team_stats_panel import BasketballStatsPanel
from .title_panel import TitlePanel



class FelsonFrame:
    _settings = {"item": None,
                 "isVisible": True,
                 }

    def __init__(self, ctrl):

        self.frameSettings = {}
        self._setFrame(ctrl)
        self._setSizers()
        self._Layout()


    def _Layout(self):
        width = 725
        height = 250
        if self.frameSettings["noteBookPanel"]["isVisible"] and self.frameSettings["logPanel"]["isVisible"]:
            width = 1050
            height = 650
            if self.frameSettings["noteBookPanel"]["page"] == "Player Stats":
                self.titlePanel.collapse()
                self.titlePanel.SetMinSize(wx.Size(750,50))
                self.noteBookPanel.SetMinSize(wx.Size(725,600))
            else:
                self.titlePanel.inflate()
                self.titlePanel.SetMinSize(wx.Size(750,200))
                self.noteBookPanel.SetMinSize(wx.Size(725,450))

        elif self.frameSettings["noteBookPanel"]["isVisible"]:
            height = 850

            if self.frameSettings["noteBookPanel"]["page"] == "Player Stats":
                self.titlePanel.collapse()
                self.titlePanel.SetMinSize(wx.Size(750,50))
                self.noteBookPanel.SetMinSize(wx.Size(725,600))
            else:
                self.titlePanel.inflate()
                self.titlePanel.SetMinSize(wx.Size(750,200))
                self.noteBookPanel.SetMinSize(wx.Size(725,450))
        elif self.frameSettings["logPanel"]["isVisible"]:
            height = 1000

        self.mainPanel.Layout()
        self.felsonFrame.SetSize(wx.Size(width,height))
        self.felsonFrame.Show()


    def _setSizers(self):
        topSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer.Add(self.titlePanel)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(topSizer)

        bodySizer = wx.BoxSizer()
        bodySizer.Add(self.noteBookPanel, 1, wx.EXPAND)
        bodySizer.Add(self.logPanel, 0, wx.EXPAND)

        mainSizer.Add(bodySizer)

        self.mainPanel.SetSizer(mainSizer)



    def _setTitlePanel(self, ctrl):
        self.titlePanel = TitlePanel(self.mainPanel, ctrl=ctrl)
        self.titlePanel.SetMinSize(wx.Size(725,200))
        self.frameSettings["titlePanel"] = self._settings.copy()


    def _setLogPanel(self, ctrl):
        self.logPanel = GameLogPanel(self.mainPanel, ctrl=ctrl)
        self.logPanel.SetMinSize(wx.Size(400,650))
        self.logPanel.Hide()
        self.frameSettings["logPanel"] = self._settings.copy()
        self.frameSettings["logPanel"]["isVisible"] = False


    def onNotebook(self, evt):
        print("onNotebook")
        print("old settings:", self.frameSettings["noteBookPanel"]["page"])
        self.frameSettings["noteBookPanel"]["page"] = self.noteBookPanel.GetPageText(self.noteBookPanel.GetSelection())
        self._Layout()
        print("new settings:", self.frameSettings["noteBookPanel"]["page"])

    def _setNotebook(self):
        # TODO: notebook panel
        self.noteBookPanel = wx.Notebook(self.mainPanel)
        self.teamStatsPanel = BasketballStatsPanel(self.noteBookPanel)
        self.noteBookPanel.AddPage(self.teamStatsPanel, "Team Stats")

        self.playerStatsPanel = PlayerStatsPanel(self.noteBookPanel)
        self.noteBookPanel.AddPage(self.playerStatsPanel, "Player Stats")

        self.noteBookPanel.SetMinSize(wx.Size(725,450))
        self.noteBookPanel.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onNotebook)

        self.noteBookPanel.Hide()
        self.frameSettings["noteBookPanel"] = self._settings.copy()
        self.frameSettings["noteBookPanel"]["isVisible"] = False
        self.frameSettings["noteBookPanel"]["page"] = self.noteBookPanel.GetPageText(self.noteBookPanel.GetSelection())


    def _setFrame(self, ctrl):

        self.felsonFrame = wx.Frame(None)
        self.mainPanel = wx.Panel(self.felsonFrame)
        self.frameSettings["felsonFrame"] = self._settings.copy()
        self.frameSettings["mainPanel"] = self._settings.copy()

        self._setTitlePanel(ctrl)
        self._setLogPanel(ctrl)
        self._setNotebook()
