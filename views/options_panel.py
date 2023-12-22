import wx


class OptionsPanel(wx.Panel):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.hA = wx.RadioBox(self, label="home/away", choices=("all", "away", "home"), name="isHome")
        self.wL = wx.RadioBox(self, label="win/loss", choices=("all", "winner", "loser"), name="isWinner")
        self.fav = wx.RadioBox(self, label="favorites", choices=("all", "favorite", "underdog"), name="isFavorite")
        self.ats = wx.RadioBox(self, label="covers", choices=("all", "cover", "loser"), name="isCover")

        optionsSizer = wx.BoxSizer()
        leftSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer = wx.BoxSizer(wx.VERTICAL)

        leftSizer.Add(self.hA, 0, wx.ALL, 5)
        leftSizer.Add(self.wL, 0, wx.ALL, 5)

        rightSizer.Add(self.fav, 0, wx.ALL, 5)
        rightSizer.Add(self.ats, 0, wx.ALL, 5)

        optionsSizer.Add(leftSizer)
        optionsSizer.Add(rightSizer)

        self.SetSizer(optionsSizer)
