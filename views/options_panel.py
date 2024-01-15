import wx


class OptionsPanel(wx.Panel):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.hA = wx.RadioBox(self, label="home/away", choices=("all", "away", "home"), name="isHome")
        self.wL = wx.RadioBox(self, label="win/loss", choices=("all", "winner", "loser"), name="isWinner")
        self.fav = wx.RadioBox(self, label="favorites", choices=("all", "favorite", "underdog"), name="isFavorite")
        self.ats = wx.RadioBox(self, label="covers", choices=("all", "cover", "loser"), name="isCover")


        # self.vs = wx.Button(self, label="VS")
        self.all = wx.Button(self, label="ALL")
        self.clear = wx.Button(self, label="CLR")
        self.set = wx.Button(self, label="SET")

        buttonSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer = wx.BoxSizer()
        topSizer.Add(self.all)
        topSizer.Add(self.clear)
        buttonSizer.Add(topSizer)
        buttonSizer.Add(self.set)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        optionsSizer = wx.BoxSizer()
        leftSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer = wx.BoxSizer(wx.VERTICAL)

        leftSizer.Add(self.hA, 0, wx.ALL, 5)
        leftSizer.Add(self.wL, 0, wx.ALL, 5)

        rightSizer.Add(self.fav, 0, wx.ALL, 5)
        rightSizer.Add(self.ats, 0, wx.ALL, 5)

        optionsSizer.Add(leftSizer)
        optionsSizer.Add(rightSizer)

        mainSizer.Add(optionsSizer)
        mainSizer.Add(buttonSizer)

        self.SetSizer(mainSizer)
