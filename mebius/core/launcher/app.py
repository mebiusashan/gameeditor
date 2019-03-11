# coding=UTF-8

from ..info.info import *
from ..projectframe.ProjectManage import ProjectManage
import os
import wx


class Launcher(object):

    def __init__(self):
        self.manage = ProjectManage()

        self.app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
        self.frame = wx.Frame(None, wx.ID_ANY, TITLE, size=(600, 500))  # A Frame is a top-level window.
        self.panel = wx.Panel(self.frame)
        self.frame.Show(True)  # Show the frame.

        self.__addButton()
        self.app.MainLoop()

    def __addButton(self):
        # wx.StaticText(self.panel, label="Hello World", pos=(100, 100))
        self.openProjectBtn = wx.Button(self.panel, wx.ID_ANY, "打开项目")
        self.openProjectBtn.Bind(wx.EVT_BUTTON, self.OnOpenProjectClicked)

    def OnOpenProjectClicked(self, event):
        dlg = wx.DirDialog(self.panel, u"选择文件夹", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.openProjectWithPath(dlg.GetPath())
        dlg.Destroy()

    def openProjectWithPath(self, path):
        print("open project, path: %s" % path)
        rel = self.manage.openNewProject(path)
        if rel == False:
            dlg = wx.MessageDialog(self.frame,
                                   '当前工作空间已经打开: ' + path,
                                   '警告',
                                   wx.OK
                                   )
            dlg.ShowModal()
            dlg.Destroy()
