# coding=UTF-8

from ..info.info import *

import wx
import wx.aui as aui
import wx.html2 as webview
import os

ProjectFrameEvent_CLOSE = wx.NewEventType()  # 2 创建一个事件类型
EVT_Project_Frame = wx.PyEventBinder(ProjectFrameEvent_CLOSE, 1)  # 3 创建一个绑定器对象


class ProjectFrameEvent(wx.PyCommandEvent):  # 1 定义事件
    def __init__(self, evtType, id):
        wx.PyCommandEvent.__init__(self, evtType, id)

    def SetProjectID(self, id):
        self.FrameID = id


class ProjectFrame(wx.EvtHandler):
    def __init__(self, path, id):
        super(ProjectFrame, self).__init__()
        self.FrameID = id
        self.projectPath = path
        self.frame = wx.Frame(None, wx.ID_ANY, TITLE + " - " + path, size=(1000, 800))
        self.frame.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.mgr = wx.aui.AuiManager(self.frame)

        self.leftpanel = wx.Panel(self.frame, -1, size=(200, 150))
        self.rightpanel = wx.Panel(self.frame, -1, size=(200, 150))
        self.bottompanel = wx.Panel(self.frame, -1, size=(200, 150))

        self.mgr.AddPane(self.rightpanel, wx.aui.AuiPaneInfo().Caption("工具").Center().Layer(2))
        self.mgr.AddPane(self.bottompanel, wx.aui.AuiPaneInfo().Caption("输出").Bottom().Layer(1))
        self.mgr.AddPane(self.leftpanel, wx.aui.AuiPaneInfo().Caption("目录").Left().Layer(1))

        # 输出框
        self.t3 = wx.TextCtrl(self.bottompanel, -1,
                              "输出...",
                              size=(200, 100), style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)

        self.t3.SetInsertionPoint(0)
        self.addOutput("workspace: " + path)
        # self.Bind(wx.EVT_TEXT, self.EvtText, t3)
        # self.Bind(wx.EVT_TEXT_ENTER, self.EvtTextEnter, t3)

        sizer = wx.BoxSizer()
        sizer.Add(self.t3, 1, wx.EXPAND)
        self.bottompanel.SetSizer(sizer)
        wx.CallAfter(self.bottompanel.SendSizeEvent)

        # self.dir = wx.FileCtrl(self.frame, wx.ID_ANY, defaultDirectory=path, style=wx.FC_DEFAULT_STYLE, size=(800, 600))
        self.dir = wx.GenericDirCtrl(self.leftpanel, wx.ID_ANY, dir=path, style=wx.DIRCTRL_SELECT_FIRST,
                                     size=(400, 600))
        self.dir.ShowHidden(False)

        # 文件列表
        tree = self.dir.GetTreeCtrl()
        self.frame.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.dirBrowser_OnItemSelected, tree)

        sizer = wx.BoxSizer()
        sizer.Add(tree, 1, wx.EXPAND)
        self.leftpanel.SetSizer(sizer)
        wx.CallAfter(self.leftpanel.SendSizeEvent)

        # 工具框，里面可添加任意的工具面板
        self.nb = aui.AuiNotebook(self.rightpanel)
        # page = wx.TextCtrl(self.nb, -1, "Welcome", style=wx.TE_MULTILINE)
        # self.addToolPanel(page, "Welcome")
        wv = webview.WebView.New(self.nb)
        wv.LoadURL(os.path.abspath(os.curdir) + "/welcome/index.htm")
        self.addToolPanel(wv, "Welcome")

        self.mgr.Update()

    def show(self):
        self.frame.Show(True)

    def OnCloseWindow(self, event):
        evt = ProjectFrameEvent(ProjectFrameEvent_CLOSE, 0)
        evt.SetProjectID(self.FrameID)
        self.ProcessEvent(evt)
        self.frame.Destroy()

    def dirBrowser_OnItemSelected(self, event):
        print("CLicked", self.dir.GetFilePath())
        # win = wx.MDIChildFrame(self.frame, wx.ID_ANY, "Child Window")
        # win.Show(True)
        # self.addToolPanel()
        self.addOutput("open file:" + self.dir.GetFilePath())
        self.mgr.Update()

    def addToolPanel(self, page, title):
        self.nb.AddPage(page, title)
        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.rightpanel.SetSizer(sizer)
        wx.CallAfter(self.nb.SendSizeEvent)

    def addOutput(self, text):
        self.t3.write("\n")
        self.t3.write(text)
