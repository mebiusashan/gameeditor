# coding=UTF-8

class ExcelMeta(object):
    def __init__(self):
        self.hasErr = False;
        self.err = None;
        self.wb = None;
        self.myExcel: MyExcel = None;

    def __str__(self):
        if self.hasErr:
            return "error:" + str(self.err)
        return str(self.myExcel)


class MyExcel(object):
    def __init__(self):
        self.defConfig: DefConfig = DefConfig()
        self.idTypes = []  # type: list[IDType]
        self.sheets = {}  # type: dict[str,SheetData]

    def addIDType(self, num, className, strName):
        vo = IDType()
        vo.addIDType(num, className, strName)
        self.idTypes.append(vo)

    def addSheet(self, key, sheet):
        self.sheets[key] = sheet

    def getSheetDataByNameAndID(self, name, id):
        for key in self.sheets:
            if key == name:
                # print(self.sheets[key].datas, name, id)
                datas = self.sheets[key].datas
                for i in datas:
                    if i['id'] == id:
                        return i
        return None

    def __str__(self):
        strs = str(self.typeVO)
        strs += "\nidTypes:\n"
        for i in self.idTypes:
            strs += ' --' + str(i) + "\n"
        strs += "structureData:\n"
        for key in self.structureData:
            strs += '..................\n' + str(self.structureData[key])
        return strs


class DefConfig(object):
    '''
    默认的配置数据，来源于config SHEET
    ID类型的记录数据
    typelen为ID类型的最长长度
    typeloc为每一类ID中，的最长长度
    通过以下公式来判定ID所属的类型
    类型范围 = typelen / typeloc
    这组数据存储在config表中
    '''

    def __init__(self):
        self.typelen: int = 0;
        self.loc: int = 0;

    def addTypeLen(self, typelen, loc):
        self.typelen = typelen
        self.loc = loc

    def __str__(self):
        return "typelen:" + str(self.typelen) + " loc:" + str(self.loc)


class IDType(object):
    '''
    默认的配置数据，来源于id_type SHEET
    ID类型表
    num为类型范围值
    className是对应该类型的结构体名称
    strName是对应的中文名
    这组数据存储在id_type表中
    '''

    def __init__(self):
        self.num = 0;
        self.className = "";
        self.strName = "";

    def addIDType(self, num, className, strName):
        self.num = num
        self.className = className
        self.strName = strName

    def __str__(self):
        return "num:" + str(self.num) + " className:" + self.className + " strName:" + self.strName


class SheetData(object):
    '''
    将一个sheet转换为此结构
    一个数据表的结构定义
    type表示当前这个结构体对应的id_type表中类型id
    name表示当前表的名称
    export表示当前表是否导出
    structs表示当前表结构
    datas表示当前表中的数据
    '''

    def __init__(self):
        self.type = 0;
        self.name = "";
        self.export = True;
        self.sheetStruct = []  # type: list[SheetStruct];
        self.datas = [];

    def setSheetConfig(self, type, name, export):
        self.type = type
        self.name = name
        self.export = export == 'yes' if True else False

    def addSheetStruct(self, key, datatype, name, exptype, des, index):
        struct = SheetStruct()
        struct.setData(key, datatype, name, exptype, des, index)
        self.sheetStruct.append(struct)

    def addData(self, data):
        self.datas.append(data)

    def getDataTypeByKey(self, key):
        for i in self.sheetStruct:
            if i.key == key:
                return i.datatype
        return None

    def getExportByKey(self, key):
        for i in self.sheetStruct:
            if i.key == key:
                return i.exptype
        return None


class SheetStruct(object):
    '''
    一个sheet的结构定义
    表中的结构定义
    key:对应的名称 第2行
    datatype:对应的数据类型 第3行
    name:名称 第4行
    exptype:导出的类型（export为值导出,noexport不导出,exportin引用数据导出）第5行
    des:name字段中的描述内容 第5行中的注释
    index:是否为索引 第6行
    '''

    def __init__(self):
        self.key = "";
        self.datatype = "";
        self.name = "";
        self.exptype = "export";
        self.des = "";
        self.index = False;

    def setData(self, key, datatype, name, exptype, des, index):
        self.key = key
        self.datatype = datatype
        self.name = name
        self.exptype = exptype
        self.des = des
        self.index = index == "index" if True else False

    def __str__(self):
        return "{'key': '" + self.key + "', 'dataType: '" + self.datatype + "', 'name: '" + self.name + "', 'exptype: '" + self.exptype + "'}";
