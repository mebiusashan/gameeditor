# coding=UTF-8

from mebius.plugin.excel2json.read.readexcel import open
from mebius.plugin.excel2json.write.export import export

path = '/Users/mebius/Desktop/bbb/'
rel = open("/Users/mebius/Documents/game/feidao.xlsx")
export(rel.myExcel, "b", path)
