# coding=UTF-8

from .ProjectFrame import ProjectFrame, EVT_Project_Frame
import wx


class ProjectManage(object):
    def __init__(self):
        self.curID = 0;
        self.frames = []  # type: list[ProjectFrame]

    def openNewProject(self, path):
        for i in self.frames:
            if i.projectPath == path:
                print("%s 项目已打开" % path)
                return False
        frame = ProjectFrame(path, self.curID)
        self.curID += 1;
        frame.Bind(EVT_Project_Frame, self.OnCloseWindow)
        self.frames.append(frame)
        frame.show()
        return True

    def OnCloseWindow(self, event):
        # print(self, event, event.FrameID)
        frameID = event.FrameID
        for i in self.frames:
            if i.FrameID == frameID:
                self.frames.remove(i)
                return
