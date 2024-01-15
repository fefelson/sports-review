import matplotlib
matplotlib.use('WXAgg')

import wx

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

from ..events import EVT_Tracking
from ..helpers import closest_named_color



class ChartPanel(wx.Panel):

    _figHeight = None
    _figWidth = None

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.figure = Figure()
        self.figure.set_figheight(self._figHeight)
        self.figure.set_figwidth(self._figWidth)
        self.axes = self.figure.subplots(1,1)
        self.canvas = FigureCanvas(self, -1, self.figure)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(sizer)




class LineChart(ChartPanel):

    _figHeight = 2
    _figWidth = 6

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)


    def setPanel(self, info):

        self.axes.clear()
        self.axes.plot(range(len(info["postLines"])), info["postLines"])
        self.axes.grid(True)

        self.canvas.draw()
        self.canvas.Refresh()
        self.Layout()






class BarChart(ChartPanel):

    _aLabel = "Home"
    _bLabel = "Away"
    _discriminator = "isHome"
    _figHeight = 4
    _figWidth = 6
    _lowerBound = -40
    _upperBound = 40
    _selector = "result"
    _title = None
    _xLabel = None
    _yLabel = None

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)


    def dataMaker(self, gameLog):
        aList = []
        bList = []
        for i, mO in enumerate(gameLog):
            if mO[self._discriminator] == 1:
                aList.append((i, mO[self._selector]))
            else:
                bList.append((i, mO[self._selector]))
        data = [mO[self._selector] for mO in gameLog if mO[self._selector] != None]
        return aList, bList, data


    def setColors(self, team):
        return [closest_named_color(x) for x in team.getColors()]


    def setPanel(self, team):

        aColor, bColor = self.setColors(team)
        aList = []
        bList = []
        gameLog = sorted(team.getGameLog(), key=lambda x: x["gameDate"])
        num = [x for x in range(len(gameLog))]

        aList, bList, data = self.dataMaker(gameLog)

        a,b = 6,13

        twoWeek = [sum(data[(i-a):i])/a for i in range(a,len(data)+1)]
        oneMonth = [sum(data[(i-b):i])/b for i in range(b,len(data)+1)]
        start = len(data) - 25 if len(data) - 25 > 0  else 0
        end = len(data)+3


        self.axes.clear()
        self.axes.bar([x[0] for x in aList], [x[1] for x in aList], color=[aColor for x in aList], label=self._aLabel)
        self.axes.bar([x[0] for x in bList], [x[1] for x in bList], color=[bColor for x in bList], label=self._bLabel)
        self.axes.grid(True)
        self.axes.axis([start, end, min(data)-10 max(data)+10)
        self.axes.plot([i for i in range(a,len(data)+1)], twoWeek, color="green", label="{:2d} GMA {:.1f}".format(a, twoWeek[-1]))
        self.axes.plot([i for i in range(b,len(data)+1)], oneMonth, color="gold", label="{:2d} GMA {:.1f}".format(b, oneMonth[-1]))
        self.axes.legend(loc="lower left")
        self.figure.suptitle(self._title)
        self.axes.set_xlabel(self._xLabel)
        self.axes.set_ylabel(self._yLabel)


        self.canvas.draw()
        self.canvas.Refresh()
        self.Layout()



class WinLossChart(BarChart):

    _aLabel = "Home"
    _bLabel = "Away"
    _discriminator = "isHome"
    _lowerBound = -40
    _upperBound = 40
    _selector = "result"
    _title = "Win / Loss"
    _xLabel = 'game date'
    _yLabel = 'game result'


    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
















class WinROIChart(BarChart):

    _aLabel = "Home"
    _bLabel = "Away"
    _discriminator = "isWinner"
    _lowerBound = -400
    _upperBound = 400
    _selector = "money"
    _title = "WinROI"
    _xLabel = 'game date'
    _yLabel = 'money returned'


    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)


    def dataMaker(self, gameLog):
        aList = []
        bList = []
        for i, mO in enumerate(gameLog):
            if mO[self._selector]:
                if mO[self._discriminator]:
                    if mO[self._selector] > 0:
                        aList.append((i, 100+int(mO[self._selector])))
                    else:
                        aList.append((i, 100+ ((10000/mO[self._selector])*100)))
                else:
                    bList.append((i, -100))
        data = [mO[self._selector] for mO in gameLog if mO[self._selector] != None]
        return aList, bList, data



class ChartFrame(wx.Frame):

    _chartPanel = None

    def __init__(self, parent, teamIds=[], *args, **kwargs):
        super().__init__(parent, size=(600,500), *args, **kwargs)
        self.Bind(EVT_Tracking, self.setPanel)

        panel = wx.Panel(self)
        self.title = wx.StaticText(panel, label="")
        self.chart = self._chartPanel(panel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.title, 0, wx.CENTER)
        sizer.Add(self.chart, 0, wx.ALL, 10)
        panel.SetSizer(sizer)


    def setPanel(self, evt):
        team = evt.GetValue()
        self.title.SetLabel("{}".format(team.getInfo("lastName")))
        self.chart.setPanel(team)
        self.Fit()
        self.Layout()


class DoubleFrame(wx.Frame):

    _spreadChart = None
    _coverChart = None

    def __init__(self, parent, teamIds=[], *args, **kwargs):
        super().__init__(parent, size=(850,500), *args, **kwargs)
        self.Bind(EVT_Tracking, self.setPanel)

        panel = wx.Panel(self)
        self.title = wx.StaticText(panel, label="Team Name ATS/COVERs")
        self.pointSpreadChart = self._spreadChart(panel)
        self.coverChart = self._coverChart(panel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.title, 0, wx.CENTER)
        sizer.Add(self.pointSpreadChart, 0, wx.ALL, 10)
        sizer.Add(self.coverChart, 0, wx.ALL, 10)
        panel.SetSizer(sizer)


    def setPanel(self, evt):
        team = evt.GetValue()
        self.title.SetLabel("{}".format(team.getInfo("lastName")))
        self.pointSpreadChart.setPanel(team)
        self.coverChart.setPanel(team)
        self.Fit()
        self.Layout()
