import wx



class TagPanel(wx.Panel):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        b2bBox = wx.StaticBox(self)
        self.b2b = wx.StaticText(self, label=" B2B ")
        self.b2b.SetBackgroundColour(wx.Colour("black"))
        self.b2b.SetForegroundColour(wx.Colour("white"))
        self.b2b.Hide()

        b2bSizer = wx.StaticBoxSizer(b2bBox)
        b2bSizer.Add(self.b2b, 0, wx.CENTER)


        risingBox = wx.StaticBox(self)
        self.rising = wx.StaticText(self, label="Rising")
        self.rising.SetBackgroundColour(wx.Colour("orange"))
        self.rising.SetForegroundColour(wx.Colour("white"))
        self.rising.Hide()

        risingSizer = wx.StaticBoxSizer(risingBox)
        risingSizer.Add(self.rising, 0, wx.CENTER)


        fallingBox = wx.StaticBox(self)
        self.falling = wx.StaticText(self, label="Falling")
        self.falling.SetBackgroundColour(wx.Colour("purple"))
        self.falling.SetForegroundColour(wx.Colour("white"))
        self.falling.Hide()

        fallingSizer = wx.StaticBoxSizer(fallingBox)
        fallingSizer.Add(self.falling, 0, wx.CENTER)


        moneyBox = wx.StaticBox(self)
        self.money = wx.StaticText(self, label="$MONEY$")
        self.money.SetBackgroundColour(wx.Colour("gold"))
        self.money.SetForegroundColour(wx.Colour("black"))
        self.money.Hide()

        moneySizer = wx.StaticBoxSizer(moneyBox)
        moneySizer.Add(self.money, 0, wx.CENTER)


        atsBox = wx.StaticBox(self)
        self.ats = wx.StaticText(self, label="$ATS$")
        self.ats.SetBackgroundColour(wx.Colour("green"))
        self.ats.SetForegroundColour(wx.Colour("gold"))
        self.ats.Hide()

        atsSizer = wx.StaticBoxSizer(atsBox)
        atsSizer.Add(self.ats, 0, wx.CENTER)



        totalBox = wx.StaticBox(self)
        self.total = wx.StaticText(self, label="$TOTAL$")
        self.total.SetBackgroundColour(wx.Colour("tan"))
        self.total.SetForegroundColour(wx.Colour("white"))
        self.total.Hide()

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


    def setPanel(self, team):

        if team.b2B:
            self.b2b.Show()


        winColor, _ = team.getValueColor("teamMoneyROI", team.getOdds("teamMoneyROI"))
        if winColor == "gold":
            self.money.Show()
        elif winColor == "red":
            self.money.Show()
            self.money.SetBackgroundColour(wx.Colour("black"))
            self.money.SetForegroundColour(wx.Colour("white"))


        atsColor, _ = team.getValueColor("cover%", team.getRecords("cover%"))
        if atsColor == "gold":
            self.ats.Show()
        elif atsColor == "red":
            self.ats.Show()
            self.ats.SetBackgroundColour(wx.Colour("black"))
            self.ats.SetForegroundColour(wx.Colour("white"))


        oUColor, _ = team.getValueColor("overROI", team.getOdds("overROI"))
        if oUColor == "gold":
            self.total.Show()
            self.total.SetLabel("$OVER$")
            self.total.SetBackgroundColour(wx.Colour("red"))
            self.total.SetForegroundColour(wx.Colour("white"))
        oUColor, _ = team.getValueColor("underROI", team.getOdds("underROI"))
        if oUColor == "gold":
            self.total.Show()
            self.total.SetLabel("$UNDER$")
            self.total.SetBackgroundColour(wx.Colour("blue"))
            self.total.SetForegroundColour(wx.Colour("white"))

        self.Layout()
