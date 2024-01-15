import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar2Wx
import wx

from .base_panel import BasePanel

from ..events import EVT_Total



class ChartPanel(wx.Panel):

    _trackLimits = None
    _colors = None

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.figure = Figure()
        self.figure.set_figheight(2)
        self.figure.set_figwidth(6)
        self.axes = self.figure.subplots(1,1)
        self.canvas = FigureCanvas(self, -1, self.figure)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(sizer)


    def setPanel(self, info):

        self.axes.clear()
        self.axes.plot(range(len(info["postLines"])), info["postLines"])
        self.axes.grid(True)

        self.canvas.draw()
        self.canvas.Refresh()
        self.Layout()


class HistPanel(wx.Panel):



    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.figure = Figure()
        self.figure.set_figheight(2)
        self.figure.set_figwidth(4)
        self.axes = self.figure.subplots(1,1)
        self.canvas = FigureCanvas(self, -1, self.figure)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(sizer)



    def setPanel(self, info):

        self.axes.clear()
        try:
            n, bins, patches = self.axes.hist(info["spreadBoxes"], len(info["spreadCount"].keys()))

            for item,patch in zip(bins,patches):
                if item < info["oU"] :
                    patch.set_facecolor("blue")
                elif item == info["oU"]:
                    patch.set_facecolor("orange")
                elif item > info["oU"]:
                    patch.set_facecolor("red")


            self.canvas.draw()
            self.canvas.Refresh()
        except:
            pass


class WritingPanel(BasePanel):

    def __init__(self, parent, teamIds=[], *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.title = self.createStaticText(self, label="Title", fontSize=12, bold=True)
        self.teams = {}
        self.values = {"away":{}, "home":{}}

        for hA in ("away", "home"):
            self.teams[hA] = wx.StaticText(self, label="{} {}".format(hA.upper(), "N"))
            for key in ("over%", "overROI", "under%", "underROI", "oU",
                        "total"):
                self.values[hA][key] = wx.StaticText(self, label=key)

        gamesLabel = wx.StaticText(self, label="Games in Set:")
        self.gameNum = wx.StaticText(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.title, 0, wx.TOP | wx.BOTTOM | wx.CENTER, 10)

        mainSizer = wx.GridSizer(cols=3,vgap=5, hgap=5)
        mainSizer.Add(self.teams["away"])
        mainSizer.Add(wx.StaticLine(self))
        mainSizer.Add(self.teams["home"])

        mainSizer.Add(self.values["away"]["over%"])
        mainSizer.Add(self.createStaticText(self, "OVER %", 12, True))
        mainSizer.Add(self.values["home"]["over%"])

        mainSizer.Add(self.values["away"]["overROI"])
        mainSizer.Add(self.createStaticText(self, "OVER ROI%", 12, True))
        mainSizer.Add(self.values["home"]["overROI"])

        mainSizer.Add(self.values["away"]["under%"])
        mainSizer.Add(self.createStaticText(self, "Under %", 12, True))
        mainSizer.Add(self.values["home"]["under%"])

        mainSizer.Add(self.values["away"]["underROI"])
        mainSizer.Add(self.createStaticText(self, "UNDER ROI%", 12, True))
        mainSizer.Add(self.values["home"]["underROI"])

        mainSizer.Add(self.values["away"]["oU"])
        mainSizer.Add(self.createStaticText(self, "oU Med", 12, True))
        mainSizer.Add(self.values["home"]["oU"])

        mainSizer.Add(self.values["away"]["total"])
        mainSizer.Add(self.createStaticText(self, "Total Med", 12, True))
        mainSizer.Add(self.values["home"]["total"])

        mainSizer.Add(gamesLabel)
        mainSizer.Add(self.gameNum)

        sizer.Add(mainSizer, 1, wx.CENTER)

        self.SetSizer(sizer)
        self.Layout()


    def setPanel(self, info):
        self.gameNum.SetLabel(str(info["gp"]))

        for hA in ("away", "home"):
            self.teams[hA].SetLabel("{} {}".format(hA, info[hA]["ML"]))
            self.values[hA]["over%"].SetLabel("{:.0f}%".format(info[hA]["over%"]))
            self.values[hA]["under%"].SetLabel("{:.0f}%".format(info[hA]["under%"]))
            self.values[hA]["overROI"].SetLabel("{:.0f}%".format(info[hA]["overROI"]))
            self.values[hA]["underROI"].SetLabel("{:.0f}%".format(info[hA]["underROI"]))
            self.values[hA]["oU"].SetLabel("{:.1f}".format(info[hA]["oU"]))
            self.values[hA]["total"].SetLabel("{:.1f}".format(info[hA]["total"]))



class TotalFrame(wx.Frame):

    def __init__(self, parent, teamIds=[], *args, **kwargs):
        super().__init__(parent, size=(900,800), *args, **kwargs)
        self.Bind(EVT_Total, self.setPanel)

        self.panel = BasePanel(self)
        self.title = wx.StaticText(self.panel)
        self.chart = ChartPanel(self.panel)

        self.hist1 = HistPanel(self.panel)
        self.writ1 = WritingPanel(self.panel)

        self.hist2 = HistPanel(self.panel)
        self.writ2 = WritingPanel(self.panel)


        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.title, 0, wx.CENTER)
        sizer.Add(self.chart, 0, wx.CENTER)
        sizer.Add(wx.StaticLine(self.panel, size=(-1,10)), 0, wx.BOTTOM, 10)

        bodySizer = wx.BoxSizer()

        leftSizer = wx.BoxSizer(wx.VERTICAL)
        leftSizer.Add(self.hist1)
        leftSizer.Add(wx.StaticLine(self.panel, size=(-1,10)))
        leftSizer.Add(self.hist2)
        bodySizer.Add(leftSizer, 1)

        rightSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer.Add(self.writ1)
        rightSizer.Add(wx.StaticLine(self.panel, size=(-1,10)))
        rightSizer.Add(self.writ2)
        bodySizer.Add(rightSizer, 1)

        sizer.Add(bodySizer, 1)

        self.panel.SetSizer(sizer)



    def setPanel(self, evt):
        info = evt.GetValue()
        oU = str(float(info["oU"]))
        self.title.SetLabel("{}".format(oU))
        self.chart.setPanel(info)

        if info["homeMoney/awayMoney"]:
            self.hist1.setPanel(info["homeMoney/awayMoney"]["home"])
            self.writ1.setPanel(info["homeMoney/awayMoney"])
            self.writ1.title.SetLabel("exact match")

        self.hist2.setPanel(info["teamTotal"]["home"])
        self.writ2.setPanel(info["teamTotal"])
        self.writ2.title.SetLabel("point total match")
