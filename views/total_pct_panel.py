
import wx

from .chart_panel import DoubleFrame, BarChart


class OUChart(BarChart):

    _aLabel = "Home"
    _bLabel = "Away"
    _figHeight = 2
    _figWidth = 6
    _discriminator = "isHome"
    _lowerBound = 0
    _upperBound = 300
    _selector = "o/u"
    _title = "OVER / UNDERS"
    _xLabel = 'game date'
    _yLabel = 'O/U'


    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)


    def dataMaker(self, gameLog):
        aList = []
        bList = []
        for i, mO in enumerate(gameLog):
            if mO[self._selector]:
                if mO[self._discriminator]:
                    aList.append((i, mO[self._selector]))
                else:
                    bList.append((i, mO[self._selector]))
            data = [mO[self._selector] for mO in gameLog if mO[self._selector] != None]
        return aList, bList, data


class TotalChart(BarChart):

    _aLabel = "OVERS"
    _bLabel = "UNDERS"
    _discriminator = "isOver"
    _figHeight = 2
    _figWidth = 6
    _lowerBound = -40
    _upperBound = 40
    _selector = "o/u"
    _title = "Totals"
    _xLabel = 'game date'
    _yLabel = 'game result'


    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

    def setColors(self, team):
        return ["red", "blue"]


    def dataMaker(self, gameLog):
        aList = []
        bList = []
        for i, mO in enumerate(gameLog):
            if mO[self._selector]:
                if int(mO["total"]) - int(mO[self._selector]) > 0:
                    aList.append((i, int(mO["total"]) - int(mO[self._selector])))
                else:
                    bList.append((i, int(mO["total"]) - int(mO[self._selector])))
        data = [int(mO["total"]) - int(mO[self._selector]) for mO in gameLog if mO[self._selector] != None]
        return aList, bList, data


class TotalTrackFrame(DoubleFrame):

    _spreadChart = OUChart
    _coverChart = TotalChart
