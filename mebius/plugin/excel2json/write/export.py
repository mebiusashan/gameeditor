# coding=UTF-8
from mebius.core.fileutil.file import createAndWrite
from mebius.plugin.excel2json.data.vo import MyExcel

from .lang.json import JsonLanguage
from .lang.typescript import TypescriptLanguage


def export(myExcel: MyExcel, fileName, path):
    json = JsonLanguage()
    jsonData = json.export(myExcel, fileName)
    for i in jsonData:
        createAndWrite(path + i.subdirectory, i.fileName, i.extensionName, i.content)
    ts = TypescriptLanguage()
    tsData = ts.export(myExcel, fileName)
    for i in tsData:
        createAndWrite(path + i.subdirectory, i.fileName, i.extensionName, i.content)
