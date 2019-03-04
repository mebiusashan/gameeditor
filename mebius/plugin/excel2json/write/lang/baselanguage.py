# coding=UTF-8

class LanguageExport(object):
    def __init__(self):
        self.fileName = ""
        self.extensionName = ""
        self.content = ""
        self.subdirectory = "/"


class BaseLanguage(object):
    def export(self, fileName):
        rel = []  # type: list[LanguageExport]
        return rel
