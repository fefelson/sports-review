import wx


class BasePanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)


    def xSizer(self, text, item):
        label = wx.StaticText(self, label=text)
        label.SetFont( wx.Font(wx.FontInfo(10)))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(label, 0, wx.CENTER | wx.BOTTOM, 5)
        sizer.Add(item, 0, wx.CENTER)
        return sizer


    def createStaticText(self, parent, label, fontSize, bold):
        staticText = wx.StaticText(parent, style=wx.ALIGN_CENTRE_HORIZONTAL, label=label)
        if bold:
            staticText.SetFont(wx.Font(wx.FontInfo(fontSize).Bold()))
        else:
            staticText.SetFont(wx.Font(wx.FontInfo(fontSize)))

        return staticText
