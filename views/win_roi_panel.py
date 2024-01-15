import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import wx

from .base_panel import BasePanel

from ..events import EVT_Tracking
from ..helpers import closest_named_color




    def setPanel(self, team):

        win,loss = [closest_named_color(x) for x in team.getColors()]
        gameLog = sorted(team.getGameLog(), key=lambda x: x["gameDate"])
        num = [x for x in range(len(gameLog))]
        colors = []

        for mO in gameLog:
            if mO["isHome"] == 1:
                colors.append(win)
            else:
                colors.append(loss)

        a,b = 6,13
        data = []


        twoWeek = [sum(data[(i-a):i])/a for i in range(a,len(data)+1)]
        oneMonth = [sum(data[(i-b):i])/b for i in range(b,len(data)+1)]
        start = len(data) - 25 if len(data) - 25 > 0  else 0
        end = len(data)+3


        self.axes.clear()
        self.axes.bar(num, data, color=colors)
        self.axes.grid(True)
        self.axes.axis([start, end, -150, max(data)+5])
        self.axes.plot([i for i in range(a,len(data)+1)], twoWeek, color="blue")
        self.axes.plot([i for i in range(b,len(data)+1)], oneMonth, color="orange")
        try:
            self.axes.text(end-3, max(data)-15, "{:2d} GMA {:.1f}".format(b, oneMonth[-1]), ha='left')
        except:
            pass
        try:
            self.axes.text(end-3, max(data)-100, "{:2d} GMA {:.1f}".format(a, twoWeek[-1]), ha='left')
        except:
            pass


        self.canvas.draw()
        self.canvas.Refresh()
        self.Layout()




class WinROIFrame(wx.Frame):

    def __init__(self, parent, teamIds=[], *args, **kwargs):
        super().__init__(parent, size=(600,275), *args, **kwargs)
        self.Bind(EVT_Tracking, self.setPanel)

        panel = wx.Panel(self)
        self.title = wx.StaticText(panel, label="Team Name WinROI")
        self.chart = ChartPanel(panel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.title, 0)
        sizer.Add(self.chart, 0, wx.ALL, 10)
        panel.SetSizer(sizer)





    def setPanel(self, evt):
        team = evt.GetValue()
        self.title.SetLabel("{} Win ROI".format(team.getInfo("lastName")))
        self.chart.setPanel(team)
        self.Layout()
