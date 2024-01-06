import wx



class TagPanel(wx.Panel):

    def __init__(self, parent, ctrl=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        b2bBox = wx.StaticBox(self)
        self.b2b = wx.StaticText(self, label="B2B")
        self.b2b.SetBackgroundColour(wx.Colour("red"))
        self.b2b.SetForegroundColour(wx.Colour("white"))
        self.b2b.Bind(wx.EVT_LEFT_DCLICK, ctrl.onB2B)

        b2bSizer = wx.StaticBoxSizer(b2bBox)
        b2bSizer.Add(self.b2b, 0, wx.CENTER)


        risingBox = wx.StaticBox(self)
        self.rising = wx.StaticText(self, label="Rising")
        self.rising.SetBackgroundColour(wx.Colour("orange"))
        self.rising.SetForegroundColour(wx.Colour("white"))
        self.rising.Bind(wx.EVT_LEFT_DCLICK, ctrl.onRising)

        risingSizer = wx.StaticBoxSizer(risingBox)
        risingSizer.Add(self.rising, 0, wx.CENTER)


        fallingBox = wx.StaticBox(self)
        self.falling = wx.StaticText(self, label="Falling")
        self.falling.SetBackgroundColour(wx.Colour("purple"))
        self.falling.SetForegroundColour(wx.Colour("white"))
        self.falling.Bind(wx.EVT_LEFT_DCLICK, ctrl.onFalling)

        fallingSizer = wx.StaticBoxSizer(fallingBox)
        fallingSizer.Add(self.falling, 0, wx.CENTER)


        moneyBox = wx.StaticBox(self)
        self.money = wx.StaticText(self, label="$MONEY$")
        self.money.SetBackgroundColour(wx.Colour("gold"))
        self.money.SetForegroundColour(wx.Colour("purple"))
        self.money.Bind(wx.EVT_LEFT_DCLICK, ctrl.onMoney)

        moneySizer = wx.StaticBoxSizer(moneyBox)
        moneySizer.Add(self.money, 0, wx.CENTER)


        atsBox = wx.StaticBox(self)
        self.ats = wx.StaticText(self, label="$ATS$")
        self.ats.SetBackgroundColour(wx.Colour("green"))
        self.ats.SetForegroundColour(wx.Colour("white"))
        self.ats.Bind(wx.EVT_LEFT_DCLICK, ctrl.onAts)

        atsSizer = wx.StaticBoxSizer(atsBox)
        atsSizer.Add(self.ats, 0, wx.CENTER)



        totalBox = wx.StaticBox(self)
        self.total = wx.StaticText(self, label="$TOTAL$")
        self.total.SetBackgroundColour(wx.Colour("tan"))
        self.total.SetForegroundColour(wx.Colour("white"))
        self.total.Bind(wx.EVT_LEFT_DCLICK, ctrl.onTotal)

        totalSizer = wx.StaticBoxSizer(totalBox)
        totalSizer.Add(self.total, 0, wx.CENTER)




        sizer = wx.BoxSizer()
        sizer.Add(b2bSizer, 0, wx.LEFT | wx.RIGHT | wx.CENTER, 10)
        sizer.Add(risingSizer, 0, wx.LEFT | wx.RIGHT | wx.CENTER, 10)
        sizer.Add(fallingSizer, 0, wx.LEFT | wx.RIGHT | wx.CENTER, 10)
        sizer.Add(moneySizer, 0, wx.LEFT | wx.RIGHT | wx.CENTER, 10)
        sizer.Add(atsSizer, 0, wx.LEFT | wx.RIGHT | wx.CENTER, 10)
        sizer.Add(totalSizer, 0, wx.LEFT | wx.RIGHT | wx.CENTER, 10)

        self.SetSizer(sizer)
