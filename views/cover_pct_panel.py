
import wx

from .chart_panel import DoubleFrame, BarChart


class SpreadChart(BarChart):

    _aLabel = "Home"
    _bLabel = "Away"
    _discriminator = "isHome"
    _lowerBound = -40
    _upperBound = 40
    _selector = "spread"
    _title = "Point Spreads"
    _xLabel = 'game date'
    _yLabel = 'spread'


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


class ATSChart(BarChart):

    _aLabel = "ATS Win"
    _bLabel = "ATS Loss"
    _discriminator = "isCover"
    _lowerBound = -40
    _upperBound = 40
    _selector = "spread"
    _title = "ATS"
    _xLabel = 'game date'
    _yLabel = 'spread + result'


    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

    def setColors(self, team):
        return ["green", "red"]


    def dataMaker(self, gameLog):
        aList = []
        bList = []
        for i, mO in enumerate(gameLog):
            if mO[self._selector]:
                if  int(mO[self._selector]) + int(mO["result"]) > 0:
                    aList.append((i, int(mO[self._selector]) + int(mO["result"])))
                else:
                    bList.append((i, int(mO[self._selector]) + int(mO["result"])))
        data = [int(mO[self._selector]) + int(mO["result"]) for mO in gameLog if mO[self._selector] != None]
        return aList, bList, data


class CoverFrame(DoubleFrame):

    _spreadChart = SpreadChart
    _coverChart = ATSChart
