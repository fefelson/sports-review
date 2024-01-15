import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import wx

from .base_panel import BasePanel
from .chart_panel import LineChart

from ..events import EVT_GameOdds



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
                if item < 0 and item < -1*info["spread"] :
                    patch.set_facecolor("red")
                elif item > -1*info["spread"] and item <0:
                    patch.set_facecolor("orange")
                elif item > 0 and item < -1*info["spread"]:
                    patch.set_facecolor("orange")
                elif item > -1*info["spread"]:
                    patch.set_facecolor("green")


            self.canvas.draw()
            self.canvas.Refresh()
        except:
            pass


class WritingPanel(BasePanel):

    def __init__(self, parent, teamIds=[], *args, **kwargs):
        super().__init__(parent, size=(250,200), *args, **kwargs)

        self.title = self.createStaticText(self, label="Title", fontSize=12, bold=True)
        self.teams = {}
        self.values = {"away":{}, "home":{}}

        for hA in ("away", "home"):
            self.teams[hA] = wx.StaticText(self, label="{} {}".format(hA.upper(), "N"))
            for key in ("win", "cover", "spread", "result"):
                self.values[hA][key] = self.createStaticText(self, "", 8, False)

        gamesLabel = wx.StaticText(self, label="Games in Set:")
        self.gameNum = wx.StaticText(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.title, 0, wx.TOP | wx.BOTTOM | wx.CENTER, 10)

        titleSizer = wx.BoxSizer()
        titleSizer.Add(self.teams["away"], 0, wx.CENTER | wx.ALL, 5)
        titleSizer.Add(wx.StaticLine(self), 1, wx.EXPAND)
        titleSizer.Add(self.teams["home"], 0, wx.CENTER | wx.ALL, 5)

        winSizer = wx.BoxSizer()
        winSizer.Add(self.values["away"]["win"], 0, wx.CENTER)
        winSizer.Add(self.createStaticText(self, "Win%  roi:", 10, True), 1, wx.EXPAND)
        winSizer.Add(self.values["home"]["win"], 0, wx.CENTER)

        coverSizer = wx.BoxSizer()
        coverSizer.Add(self.values["away"]["cover"], 0, wx.CENTER)
        coverSizer.Add(self.createStaticText(self, "Cover%  roi:", 10, True), 1, wx.EXPAND)
        coverSizer.Add(self.values["home"]["cover"], 0, wx.CENTER)

        spreadSizer = wx.BoxSizer()
        spreadSizer.Add(self.values["away"]["spread"], 0, wx.CENTER)
        spreadSizer.Add(self.createStaticText(self, "Spread", 12, True), 1, wx.EXPAND)
        spreadSizer.Add(self.values["home"]["spread"], 0, wx.CENTER)

        resultSizer = wx.BoxSizer()
        resultSizer.Add(self.values["away"]["result"], 0, wx.CENTER)
        resultSizer.Add(self.createStaticText(self, "Result", 12, True), 1, wx.EXPAND)
        resultSizer.Add(self.values["home"]["result"], 0, wx.CENTER)

        gameSizer = wx.BoxSizer()
        gameSizer.Add(gamesLabel)
        gameSizer.Add(self.gameNum)

        sizer.Add(titleSizer, 1, wx.EXPAND)
        sizer.Add(winSizer, 1, wx.EXPAND)
        sizer.Add(coverSizer, 1, wx.EXPAND | wx.BOTTOM, 5)
        sizer.Add(spreadSizer, 1, wx.EXPAND)
        sizer.Add(resultSizer, 1, wx.EXPAND | wx.BOTTOM, 10)
        sizer.Add(gameSizer, 1, wx.EXPAND)


        self.SetSizer(sizer)
        self.Layout()


    def setPanel(self, info):
        self.gameNum.SetLabel(str(info["gp"]))

        for hA in ("away", "home"):
            self.teams[hA].SetLabel("{}\n{}".format(hA, info[hA]["ML"]))
            self.values[hA]["win"].SetLabel("{:.0f}%   {:.2f}".format(info[hA]["win%"], info[hA]["winROI"]))
            if info[hA]["winROI"] >5:
                self.values[hA]["win"].SetForegroundColour(wx.Colour("GOLD"))
            elif info[hA]["winROI"] <-5:
                self.values[hA]["win"].SetForegroundColour(wx.Colour("RED"))


            self.values[hA]["cover"].SetLabel("{:.0f}%   {:.2f}".format(info[hA]["cover%"], info[hA]["coverROI"]))
            if info[hA]["coverROI"] >5:
                self.values[hA]["cover"].SetForegroundColour(wx.Colour("GOLD"))
            elif info[hA]["coverROI"] <-5:
                self.values[hA]["cover"].SetForegroundColour(wx.Colour("RED"))


            self.values[hA]["spread"].SetLabel("{:.1f}".format(info[hA]["spread"]))
            self.values[hA]["result"].SetLabel("{:.1f}".format(info[hA]["result"]))

        self.Layout()



class GameOddsFrame(wx.Frame):

    def __init__(self, parent, teamIds=[], *args, **kwargs):
        super().__init__(parent, size=(900,800), *args, **kwargs)
        self.Bind(EVT_GameOdds, self.setPanel)

        self.panel = BasePanel(self)
        self.title = wx.StaticText(self.panel)
        self.chart = LineChart(self.panel)

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
        mL = "+"+str(int(info["teamML"])) if int(info["teamML"]) > 0 else int(info["teamML"])
        self.title.SetLabel("{}  {}  {}".format(info["fullName"], info["hA"].capitalize(), mL))
        self.chart.setPanel(info)
        hA = info["hA"]
        self.hist1.setPanel(info["homeMoney/awayMoney"][hA])
        self.writ1.setPanel(info["homeMoney/awayMoney"])
        self.writ1.title.SetLabel("exact money match")

        self.hist2.setPanel(info["teamMoney"][hA])
        self.writ2.setPanel(info["teamMoney"])
        self.writ2.title.SetLabel("{} money".format(hA.capitalize()))
        self.panel.Layout()


        self.panel.Layout()
