# coding=UTF-8
import os


def createAndWrite(path, name, ext, content):
    if os.path.exists(path) == False:
        os.makedirs(path)
    filePath = path + "/" + name + ext
    f = open(filePath, 'w')  # 清空文件内容再写
    f.write(content)
    f.close()
