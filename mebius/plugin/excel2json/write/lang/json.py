# coding=UTF-8

from .baselanguage import BaseLanguage
from .baselanguage import LanguageExport
from mebius.plugin.excel2json.data.vo import MyExcel

import json


class JsonLanguage(BaseLanguage):
    def export(self, myExcel: MyExcel, fileName):
        rel = []  # type: list[LanguageExport]
        data = {}
        for key in myExcel.sheets:
            sd = myExcel.sheets[key]
            if sd.export == False:
                continue
            data[sd.name] = [];
            for i in sd.datas:
                jsonData = {}
                # print(i)
                for k in i:
                    expType = sd.getExportByKey(k)
                    if expType == 'noexport':
                        continue
                    # pass
                    elif expType == 'export':
                        # print(sd.getDataTypeByKey(k), i[k], sd.name)
                        jsonValue = self.conversionJsonValue(sd.getDataTypeByKey(k), i[k])
                        # print(jsonValue)
                        jsonData[k] = jsonValue
                    elif expType == 'exportin':
                        referenceData = myExcel.getSheetDataByNameAndID(sd.getDataTypeByKey(k), i[k])
                        # print(referenceData)
                        jsonData[k] = referenceData
                data[sd.name].append(jsonData)
        expData = LanguageExport()
        expData.fileName = fileName
        expData.extensionName = ".json"
        expData.content = json.dumps(data)
        rel.append(expData)
        return rel

    def conversionJsonValue(self, dataType, value):
        rel = None
        if dataType == 'int':
            return int(value)
        elif dataType == 'string':
            return str(value)
        elif dataType == 'boolean':
            return value
        elif dataType == 'carr_int':
            l = str(value).split(',')
            rel = []
            for i in l:
                rel.append(int(i));
            return rel
        elif dataType == 'carr_string':
            return str(value).split(',')
        elif dataType == 'carr_boolean':
            return str(value).split(',')
        else:
            return value
