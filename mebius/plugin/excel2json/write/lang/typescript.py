# coding=UTF-8

from .baselanguage import BaseLanguage
from .baselanguage import LanguageExport
from mebius.plugin.excel2json.data.vo import MyExcel

defaultCode = '//author:A闪\n\n\n'

TypeScriptDataType = {
    'int': "number",
    'string': "string",
    'boolean': "boolean",
    'carr_int': "Array<number>",
    'carr_string': "Array<string>",
    'carr_boolean': "Array<boolean>"
}


# TODO 导出时检查导出哪里写类型，对应表中的export值未处理s

class TypescriptLanguage(BaseLanguage):
    def export(self, myExcel: MyExcel, fileName):
        rel = []  # type: list[LanguageExport]
        baseSheetCode = self.getBaseSheetCode()
        rel.append(baseSheetCode)

        modeltype = self.exportModelTypeCode(myExcel)
        rel.append(modeltype)

        gameconfigDataType = self.exportGameConfigDataTypeCode(myExcel)
        rel.append(gameconfigDataType)

        codes = self.exportTypeScriptStructureSheet(myExcel, fileName)
        rel += codes

        return rel

    def exportModelTypeCode(self, myExcel):
        ts = TypeScriptStructureSheetManage()
        modeltype = ts.toModelTypeCode(myExcel.idTypes, myExcel.defConfig.loc)
        return modeltype

    def exportGameConfigDataTypeCode(self, myExcel):
        ts = TypeScriptStructureManage()
        for key in myExcel.sheets:
            data = myExcel.sheets[key]
            # name = data.name
            ts.createData(data.name)
            # print(name, data.structs)
            for i in data.sheetStruct:
                structData = i
                expType = data.getExportByKey(structData.key)
                if expType == 'noexport':
                    continue
                # pass
                elif expType == 'export':
                    ts.addAttribute(data.name, structData.key, self.conversionDataType(structData.datatype, False))
                elif expType == 'exportin':
                    ts.addAttribute(data.name, structData.key, self.conversionDataType(structData.datatype))
        return ts.toCode()

    def exportTypeScriptStructureSheet(self, myExcel, fileName):
        ts = TypeScriptStructureSheetManage()
        for key in myExcel.sheets:
            data = myExcel.sheets[key]
            # name = data.name
            ts.createData(data.name)
            # print(name, data.structs)
            for i in data.sheetStruct:
                structData = i
                # print(data.name, structData.key, structData.datatype)
                ts.addAttributeIndex(data.name, structData.key, self.conversionDataType(structData.datatype),
                                     structData.index)
        rel = [];
        rel += ts.toSheetCode()
        rel += ts.toSheetCustomCode()
        rel.append(ts.toManageCode(fileName))
        return rel

    def conversionDataType(self, dataType, ref=True):
        if dataType in TypeScriptDataType.keys():
            return TypeScriptDataType[dataType]
        if ref == False:
            return 'number'
        return dataType

    def getBaseSheetCode(self):
        code = defaultCode;
        code += '''class BaseSheet {
    protected data: any;
    constructor(_data: any) {
        this.data = _data;
        this.initialize();
        this.initializeCustom();
    }

    protected initialize() {

    }

    protected initializeCustom() {

    }
}'''
        expData = LanguageExport()
        expData.fileName = 'BaseSheet'
        expData.extensionName = ".ts"
        expData.content = code
        return expData


class TypeScriptStructure(object):

    def __init__(self, name):
        self.name = name
        self.attributes = [];
        self.isIndex = False;

    def addAttribute(self, name, dataType):
        data = {}
        data['name'] = name
        data['type'] = dataType
        self.attributes.append(data)

    def addAttributeIndex(self, name, dataType, index):
        data = {}
        data['name'] = name
        data['type'] = dataType
        data['index'] = index
        self.attributes.append(data)

    def toCode(self):
        # print(self.name, (self.attributes))
        strs = "class " + self.name + " {\n"
        for i in self.attributes:
            strs += "\treadonly " + i['name'] + ": " + i['type'] + ";\n"
        strs += "}\n"
        return strs

    def toSheetCustomName(self):
        return self.name + "SheetCustom"

    def toSheetCustomCode(self):
        str = defaultCode
        str += "class " + self.name + "SheetCustom extends " + self.name + "Sheet {\n";
        str += "\n\tprotected initializeCustom() {\n\t\t\n"
        str += '\t}\n\n}'

        expData = LanguageExport()
        expData.fileName = self.name + "SheetCustom"
        expData.extensionName = ".ts"
        expData.content = str
        expData.subdirectory = "/custom/"
        return expData

    def toSheetName(self):
        return self.name + "Sheet"

    def toSheetCode(self):
        str = defaultCode
        str += "class " + self.name + "Sheet extends BaseSheet {\n\n";

        forstr = '';
        initstr = '';
        getstr = '';
        for i in self.attributes:
            if 'index' in i.keys():
                if i['index'] == True:
                    str += '\tprivate key' + i['name'] + 'Data: any;\n'
                    initstr += '\t\tthis.key' + i['name'] + 'Data = {};\n'
                    forstr += '\t\t\tthis.key' + i['name'] + 'Data[element.' + i['name'] + '] = element;\n'
                    getstr += '\tpublic getDataBy' + i['name'] + '(value:' + i['type'] + '): ' + self.name + ' {\n'
                    getstr += '\t\treturn this.key' + i['name'] + 'Data[value];\n'
                    getstr += '\t}\n\n'

        str += "\n\tprotected initialize() {\n"
        str += initstr;
        str += "\n\t\tthis.data.forEach(element => {\n"
        str += forstr;
        str += '\t\t});\n\t}\n\n'
        str += getstr;
        str += '}'

        expData = LanguageExport()
        expData.fileName = self.name + "Sheet"
        expData.extensionName = ".ts"
        expData.content = str
        expData.subdirectory = "/sheet/"
        return expData

    def __str__(self):
        return "<" + self.name + ">" + str(len(self.attributes))


class TypeScriptStructureManage(object):

    def __init__(self):
        self.datas = {};

    def createData(self, name):
        data = TypeScriptStructure(name)
        self.datas[name] = data

    def addAttribute(self, typeName, attName, attType):
        # print(self.datas[typeName])
        if self.datas[typeName] != None:
            self.datas[typeName].addAttribute(attName, attType)

    def toCode(self):
        strs = defaultCode
        for key in self.datas:
            # strs += str(self.datas[key])
            strs += self.datas[key].toCode() + "\n"

        expData = LanguageExport()
        expData.fileName = 'GameConfigDataType'
        expData.extensionName = ".ts"
        expData.content = strs
        return expData


class TypeScriptStructureSheetManage(TypeScriptStructureManage):
    def addAttributeIndex(self, typeName, attName, attType, index):
        if self.datas[typeName] != None:
            self.datas[typeName].addAttributeIndex(attName, attType, index)

    def toSheetCode(self):
        codes = [];
        for key in self.datas:
            rel = self.datas[key].toSheetCode()
            codes.append(rel)
        return codes

    def toSheetCustomCode(self):
        codes = [];
        for key in self.datas:
            rel = self.datas[key].toSheetCustomCode()
            codes.append(rel)
        return codes

    def toManageCode(self, resName):
        str = defaultCode
        str += "class GameConfig {\n\n"
        str += "\tprivate static self: GameConfig | null = null;\n"
        str += '''\tpublic static getInstance(): GameConfig {
        if (!GameConfig.self) {
            GameConfig.self = new GameConfig();
        }
        return GameConfig.self;
    }\n\n'''
        initstr = '';
        constructorstr = '';
        getstr = '';
        for key in self.datas:
            data = self.datas[key]
            initstr += "\tprivate _" + data.toSheetCustomName() + ": " + data.toSheetCustomName() + " | null = null;\n"
            constructorstr += "\t\tthis._" + data.toSheetCustomName() + " = new " + data.toSheetCustomName() + "(data['" + data.name + "']);\n";
            getstr += "\tpublic get " + data.toSheetCustomName() + "Data(): " + data.toSheetCustomName() + " {\n"
            getstr += "\t\treturn this._" + data.toSheetCustomName() + ";\n\t}\n\n"
        str += initstr;
        str += "\n\tprivate constructor() {\n"
        str += "\t\tconst data = RES.getRes('" + resName + "_json');\n"
        str += constructorstr
        str += "\t}\n\n"
        str += getstr;
        str += "}"

        expData = LanguageExport()
        expData.fileName = 'GameConfig'
        expData.extensionName = ".ts"
        expData.content = str
        return expData

    def toModelTypeCode(self, typeIDVO, loc):
        ll = str(loc)
        strs = defaultCode
        strs += "enum GameConfigItemType {\n"
        for i in typeIDVO:
            strs += "\tT" + i.className + ",\n"
        strs += "\tTUnknown\n}\n\n"
        strs += "class ModelType {\n\n"
        strs += "\tpublic static checkType(id: number): GameConfigItemType {\n"
        strs += "\t\tconst w: number = Math.floor(id / " + ll + ");\n"
        strs += "\t\tswitch (w) {\n"
        for i in typeIDVO:
            strs += "\t\t\tcase " + str(i.num) + ":\n"
            strs += "\t\t\t\treturn GameConfigItemType.T" + i.className + ";\n"
        strs += "\t\t}\n"
        strs += "\t\treturn GameConfigItemType.TUnknown;\n"
        strs += "\t}\n\n"
        strs += "\tpublic static getModelByID(id: number): any {\n"
        strs += "\t\tconst type = ModelType.checkType(id);\n"
        strs += "\t\tswitch (type) {\n"

        for i in typeIDVO:
            strs += "\t\t\tcase GameConfigItemType.T" + i.className + ":\n"
            strs += "\t\t\t\treturn GameConfig.getInstance()." + i.className + "SheetCustomData.getDataByid(id);\n"

        strs += "\t\t}\n"
        strs += "\t\treturn null;\n"
        strs += "\t}\n}"

        expData = LanguageExport()
        expData.fileName = 'ModelType'
        expData.extensionName = ".ts"
        expData.content = strs
        return expData
