import wx
import wx.lib.mixins.listctrl as listmix

from .base_panel import BasePanel
from .options_panel import OptionsPanel

from ..events import EVT_Overview


class OverviewListView(wx.ListView, listmix.ColumnSorterMixin):

    def __init__(self, parent, *args, **kwargs):
        wx.ListView.__init__(self, parent, *args, **kwargs)


    def GetListCtrl(self):
        return self


    def setItemMap(self, itemMap, size):
        self.itemDataMap = itemMap
        listmix.ColumnSorterMixin.__init__(self, size)


class OverviewFrame(wx.Frame):

    _moneyLabels = ("team", "gp", "win%", "ML", "moneyROI", "oppML", "oppROI")
    _spreadLabels = ("team", "gp", "cover%", "atsROI", "spread", "result")
    _totalLabels = ("team", "gp", "over%", "overROI", "underROI", "o/u", "total")

    def __init__(self, parent, teamIds=[], *args, **kwargs):
        super().__init__(parent, size=(625,400), *args, **kwargs)
        self.Bind(EVT_Overview, self.setPanel)

        self.panel = BasePanel(self)
        self.teamIds = teamIds

        self.viewOptions = wx.RadioBox(self.panel, choices=["money", "spread", "totals"], majorDimension=3, style=wx.RA_SPECIFY_COLS)
        self.viewOptions.Bind(wx.EVT_RADIOBOX, self.onViewOptions)

        self.moneyView = OverviewListView(self.panel,  style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        self.spreadView = OverviewListView(self.panel,  style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        self.spreadView.Hide()
        self.totalView = OverviewListView(self.panel,  style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        self.totalView.Hide()

        self._setViewColumns(self.moneyView, self._moneyLabels)
        self._setViewColumns(self.spreadView, self._spreadLabels)
        self._setViewColumns(self.totalView, self._totalLabels)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.viewOptions, 0, wx.CENTER | wx.BOTTOM)
        sizer.Add(self.moneyView, 1, wx.ALL|wx.EXPAND, 25)
        sizer.Add(self.spreadView, 1, wx.ALL|wx.EXPAND, 25)
        sizer.Add(self.totalView, 1, wx.ALL|wx.EXPAND, 25)
        self.panel.SetSizer(sizer)


    def _setViewColumns(self, view, labels):
        for i, label in enumerate(labels):
            view.InsertColumn(i, label)


    def onViewOptions(self, evt):
        rb = evt.GetEventObject()
        choice = rb.GetString(rb.GetSelection())
        self.moneyView.Hide()
        self.spreadView.Hide()
        self.totalView.Hide()

        if choice == "money":
            self.moneyView.Show()
        elif choice == "spread":
            self.spreadView.Show()
        elif choice == "totals":
            self.totalView.Show()
        self.panel.Layout()


    def setPanel(self, evt):
        info = evt.GetValue()

        info = [x for x in info if (x["ML"] != None and x["spread"] != None and x["o/u"] != None)]

        for key, listView, labels in (("money", self.moneyView, self._moneyLabels), ("spread", self.spreadView, self._spreadLabels),
                                ("totals", self.totalView, self._totalLabels)):
            itemMap = {}
            for i, team in enumerate(info):
                itemMap[i] = tuple([team[item] for item in labels])

            for i, team in enumerate(info):
                listView.InsertItem(i, team["team"])

                for j, label in enumerate(labels):
                    if label in ("win%", "cover%", "moneyROI", "oppROI", "over%",
                                    "atsROI", "overROI", "underROI"):
                        value = "{:2.1f}%".format(team[labels[j]])
                    else:
                        value = "{}".format(team[labels[j]])

                    listView.SetItem(i, j, value)

                listView.SetItemData(i, i)
                if team["teamId"] in self.teamIds:
                    listView.SetItemBackgroundColour(i, "#ff7436")

            listView.setItemMap(itemMap, len(labels))

        self.panel.Layout()
