
import wx

from .chart_panel import ChartFrame, WinLossChart, WinROIChart


class WinFrame(ChartFrame):

    _chartPanel = WinLossChart


class WinROIFrame(ChartFrame):

    _chartPanel = WinROIChart
