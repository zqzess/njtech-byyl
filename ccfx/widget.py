# This Python file uses the following encoding: utf-8
"""
@Time ： 2022/4/24 21:22
@Auth ： zqzess
@File ：widget.py
@IDE ：PyCharm
@Motto：亦余心之所善兮,虽九死其犹未悔
@desc : QT图形框架
"""
import os
from collections import namedtuple
from pathlib import Path
import sys
import platform

from PySide6 import QtWidgets

import utils

from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader

from model import twoTuple, Entity, fourTuple

# import twoTuple

rootPath = '/'  # 初始路径
directory = ''  # 输入路径
codeStr = ''
outFileName = 'out'  # 输出文件名
'''
#int$v,$c;$v=41;$c=15;$c=$v+4*6+($v*3)*$c+940*($v*6);if($v*89<$v)then$v=$c*479 ;elsebegin$c=$c+85;$c=$c+734;end;while($c*6>$v)do$v=$v+9;
'''

# identify = {"type": ""}, {"value": ""}
# identifyTable = []
numberList = []  # 存放源代码里所有数字的列表
identifyList = []  # 存放标识符的列表
index = 0  # 自动机的标号
word = None  # 下一个识别的单词
middleTable = []  # 中间代码（四元式）列表
table = ['']  # 四元式result列表
identifyCheckList = []  # 用于语义分析：重复定义，存放表示符


# 数据map
def addTOTable(name, type, value):
    identify = {"name": '', "type": '', "value": '0'}
    entity = Entity("identify", '', **identify)
    entity.name = name
    entity.type = type
    entity.value = value
    tmp = False
    if len(identifyList) == 0:
        identifyList.append(entity)
    else:
        for i in identifyList:
            if i.name == name:
                tmp = True
        if not tmp:
            identifyList.append(entity)


def identifyTable(name):
    identify = {"name": '', "type": '', "value": ''}
    entity = Entity("identify", '', **identify)
    entity.name = name
    return entity


def addToMiddleTable(operator, operand, operand2, result):
    four = fourTuple(operator, operand, operand2, result)
    middleTable.append(four)


def NXQ():
    return len(middleTable)


def tempVarTable():
    tmp = ''
    table.append(tmp)
    index2 = len(table) - 1
    name = 'T' + str(index2)
    return identifyTable(name)


def backPath(i, result):
    middleTable[i].result = result


def updateIdentifyTypeByName(name, type):
    for i in identifyList:
        if i.name == name:
            i.type = type
            break


def updateIdentifyValueByName(name, value):
    for i in identifyList:
        if i.name == name:
            i.value = value


def getIdentifyValueByName(name):
    for i in identifyList:
        if i.name == name:
            return i.value


# # 数据map
# def addToTable(mtype, mvalue):
#     global identify, identifyTable
#     identify['type'] = mtype
#     identify['value'] = mvalue
#     identifyTable.append(identify)


# 设置初始文件夹路径
def setDefaultPath():
    global rootPath
    sysstr = platform.system()
    if sysstr == 'Windows':
        rootPath = 'C:/'
    elif sysstr == "Linux":
        rootPath = '/'
    elif sysstr == "Darwin":
        userName = utils.get_current_user()
        rootPath = '/Users/' + userName


# 选择文件路径
def filePathSelect(self):
    global directory
    fileNamelList, filetype = QtWidgets.QFileDialog.getOpenFileNames(None, "选取文件", rootPath,
                                                                     'All Files(*);Text Files(*.txt)')
    # 多选判定
    if len(fileNamelList) > 1:
        utils.show_errorMessage('错误', '\n请不要多选')
        return 0
    # 文件是否选择判定
    if fileNamelList:
        directory = fileNamelList[0]
        utils.printLog(self.uiFile, '\t已选择输入文件:  ' + fileNamelList[0])
        self.uiFile.listWidget.clear()
        readDataFromTXT(self)
    else:
        utils.show_errorMessage('错误', '\n没有选择文件')
        utils.printLog(self.uiFile, '\t没有选择文件')


# 从txt读取数据
def readDataFromTXT(self):
    global codeStr
    try:
        # 以 utf-8 的编码格式打开指定文件
        f = open(directory, encoding="utf-8")
    except Exception as e:
        print(e)
        f = open(directory)
    else:
        codeStr = f.read() + '#'
        f.close()
        self.uiFile.listWidget_2.addItem("\n")
        utils.printLog(self.uiFile, "\t代码块")
        self.uiFile.listWidget_2.addItem("\n******************")
        self.uiFile.listWidget_2.addItem(codeStr + "\n******************\n")


# 打印至屏幕
def printToUI(self, ctype, name):
    self.uiFile.listWidget.addItem("(" + ctype + " , " + name + ")")


def printToUI2(self, string):
    self.uiFile.listWidget.addItem(string)


# 输出文件
def outPutFile(self):
    outPutPath = QtWidgets.QFileDialog.getExistingDirectory(self, "请选择输出文件保存路径...", rootPath)
    if outPutPath:
        outFilePath = str(outPutPath) + '/' + outFileName + '.txt'
        if os.path.exists(outFilePath):
            utils.printLog(self.uiFile, "\t存在同名输出文件，将执行删除操作!")
        try:
            # 以 utf-8 的编码格式打开指定文件
            f = open(outFilePath, "w", encoding="utf-8")
        except Exception as e:
            print(e)
            f = open(outFilePath, "w")
        else:
            num = 0
            for i in middleTable:
                f.write('(' + str(num) + ')' + ' ' + i.toString() + '\n')
                num += 1
            f.close()
            utils.printLog(self.uiFile, "\t输出完成!")
    else:
        utils.printLog(self.uiFile, "\t未选择输出文件路径!")
        return 0


# 启动入口
def startWork(self):
    global word, codeStr, numberList, identifyList, index, middleTable, table, identifyCheckList

    middleTable.clear()
    numberList = []
    identifyList = []
    index = 0
    middleTable = []
    table = ['']
    identifyCheckList = []
    self.uiFile.listWidget.clear()

    if codeStr:
        # utils.printLog(self.uiFile, "\t词法分析开始")
        word = nextInput(self)
        printToUI2(self, '[词]识别单词: ' + word.toString())
        parseProgarm(self)
        # # #
        tmp = ''
        for i in identifyList:
            tmp = tmp + i.name + ',' + i.type + ',' + i.value + ';'
        self.uiFile.listWidget.addItem('identify table: ' + tmp)
        tmp = ''
        for i in numberList:
            tmp = tmp + i + ','
        tmp = tmp[:-1]
        self.uiFile.listWidget.addItem('const table: ' + tmp)
        # utils.printLog(self.uiFile, "\t词法分析结束")
        printToUI2(self, '\n')
        num = 0
        for i in middleTable:
            printToUI2(self, '(' + str(num) + ')' + ' ' + i.toString())
            num += 1
        utils.printLog(self.uiFile, "\t程序执行完成!!!")
    else:
        utils.printLog(self.uiFile, "\t输入的源代码为空!!!")


# 词法分析
def nextInput(self):
    global numberList, index
    state = 1
    # index = 0
    tmpStr = ''
    count = len(codeStr)
    while index <= count:
        # for i in codeStr:
        i = codeStr[index]
        if i != '#':
            if i == ' ':
                index += 1
                continue
            if state == 1:
                tmpStr = ''
                if i == ';':
                    state = 4
                    tmpStr += i
                    index += 1
                if i == ',':
                    state = 5
                    tmpStr += i
                    index += 1
                if i == '=':
                    state = 6
                    tmpStr += i
                    index += 1
                    continue
                if i == '<':
                    state = 7
                    tmpStr += i
                    index += 1
                    continue
                if i == '>':
                    state = 8
                    tmpStr += i
                    index += 1
                    continue
                if i == '!':
                    state = 9
                    tmpStr += i
                    index += 1
                    continue
                if i == '+':
                    state = 11
                    tmpStr += i
                    index += 1
                if i == '-':
                    state = 12
                    tmpStr += i
                    index += 1
                if i == '*':
                    state = 13
                    tmpStr += i
                    index += 1
                if i == '/':
                    state = 14
                    tmpStr += i
                    index += 1
                if i == '(':
                    state = 15
                    tmpStr += i
                    index += 1
                if i == ')':
                    state = 16
                    tmpStr += i
                    index += 1
                if i == 'i':
                    state = 21
                    tmpStr += i
                    index += 1
                    continue
                if i == 't':
                    state = 25
                    tmpStr += i
                    index += 1
                    continue
                if i == 'e':
                    state = 29
                    tmpStr += i
                    index += 1
                    continue
                if i == 'b':
                    state = 35
                    tmpStr += i
                    index += 1
                    continue
                if i == 'w':
                    state = 40
                    tmpStr += i
                    index += 1
                    continue
                if i == 'd':
                    state = 45
                    tmpStr += i
                    index += 1
                    continue
                if i.isdigit():
                    # 数字
                    state = 47
                    tmpStr += i
                    index += 1
                    continue
            if (state == 1) & (i == '$'):
                state = 2
                tmpStr += i
                index += 1
                continue
            # if (state == 2) & i.isalpha():
            #     # isalpha 是否是英文字母
            #     # 此处判定是否是纯英文变量
            #     state = 3
            #     tmpStr += i
            #     index += 1
            #     continue

            # 变量命名可以有英文可以有数字，不可以局限于纯英文
            if state == 2:
                # isalpha 是否是英文字母
                # 此处判定是否是纯英文变量
                state = 3
                tmpStr += i
                index += 1
                continue
            if state == 3:
                if i.isalpha():
                    state = 3
                    tmpStr += i
                    index += 1
                    continue
                elif i.isdigit():
                    state = 3
                    tmpStr += i
                    index += 1
                    continue
                else:
                    # identifier 标识符
                    addTOTable(tmpStr, '', '')
                    return twoTuple("标识符", tmpStr)
                    # state = 1
                    # tmpStr = ''
                    # continue
            if state == 4:
                # ;号
                return twoTuple("分号", tmpStr)
                # printToUI(self, "seperator", tmpStr)
                # state = 1
                # tmpStr = ''
                # continue
            if state == 5:
                # ,号
                return twoTuple("逗号", tmpStr)
                # printToUI(self, "seperator", tmpStr)
                # state = 1
                # tmpStr = ''
                # continue
            if state == 6:
                # =号
                if i == '=':
                    state = 6
                    tmpStr += i
                    index += 1
                    continue
                else:
                    if len(tmpStr) == 1:
                        return twoTuple("赋值号", tmpStr)
                    elif len(tmpStr) == 2:
                        return twoTuple("关系运算符", tmpStr)
                    # printToUI(self, "mathOperator", tmpStr)
                    # state = 1
                    # tmpStr = ''
                    # continue
            if state == 7:
                # <号
                if i == '=':
                    state = 7
                    tmpStr += i
                    index += 1
                    continue
                else:
                    return twoTuple("关系运算符", tmpStr)
                    # printToUI(self, "logicOperator", tmpStr)
                    # state = 1
                    # tmpStr = ''
                    # continue
            if state == 8:
                # >号
                if i == '=':
                    state = 8
                    tmpStr += i
                    index += 1
                    continue
                else:
                    return twoTuple("关系运算符", tmpStr)
                    # printToUI(self, "logicOperator", tmpStr)
                    # state = 1
                    # tmpStr = ''
                    # continue
            if state == 9:
                # !号
                if i == '=':
                    state = 9
                    tmpStr += i
                    index += 1
                    continue
                else:
                    return twoTuple("关系运算符", tmpStr)
                    # printToUI(self, "logicOperator", tmpStr)
                    # state = 1
                    # tmpStr = ''
                    # continue
            if state == 11:
                # +号
                return twoTuple("加法运算符", tmpStr)
                # printToUI(self, "mathOperator", tmpStr)
                # state = 1
                # tmpStr = ''
                # continue
            if state == 12:
                # -号
                return twoTuple("减法运算符", tmpStr)
                # printToUI(self, "mathOperator", tmpStr)
                # state = 1
                # tmpStr = ''
                # continue
            if state == 13:
                # *号
                return twoTuple("乘法运算符", tmpStr)
                # printToUI(self, "mathOperator", tmpStr)
                # state = 1
                # tmpStr = ''
                # continue
            if state == 14:
                # /号
                return twoTuple("除法运算符", tmpStr)
            if state == 15:
                # (号
                return twoTuple("左括号", tmpStr)
            if state == 16:
                # )号
                return twoTuple("右括号", tmpStr)

            if (state == 21) & (i == 'n'):
                state = 22
                tmpStr += i
                index += 1
                continue
            if (state == 21) & (i == 'f'):
                state = 24
                tmpStr += i
            if (state == 22) & (i == 't'):
                state = 23
                tmpStr += i
            if state == 23:
                # int
                printToUI(self, "int", tmpStr)
                index += 1
                return twoTuple("int", tmpStr)

            if state == 24:
                # if
                index += 1
                return twoTuple("关键字if", tmpStr)

            if (state == 25) & (i == 'h'):
                state = 26
                tmpStr += i
                index += 1
                continue
            if (state == 26) & (i == 'e'):
                state = 27
                tmpStr += i
                index += 1
                continue
            if (state == 27) & (i == 'n'):
                state = 28
                tmpStr += i
            if state == 28:
                # then
                index += 1
                return twoTuple("关键字then", tmpStr)

            if (state == 29) & (i == 'l'):
                state = 30
                tmpStr += i
                index += 1
                continue
            if (state == 29) & (i == 'n'):
                state = 33
                tmpStr += i
                index += 1
                continue
            if (state == 30) & (i == 's'):
                state = 31
                tmpStr += i
                index += 1
                continue
            if (state == 31) & (i == 'e'):
                state = 32
                tmpStr += i
            if state == 32:
                # else
                index += 1
                return twoTuple("关键字else", tmpStr)
                # printToUI(self, "keyword", tmpStr)
                # state = 1
                # tmpStr = ''
                # index += 1
                # continue

            if (state == 33) & (i == 'd'):
                state = 34
                tmpStr += i
            if state == 34:
                # end
                index += 1
                return twoTuple("关键字end", tmpStr)
                # printToUI(self, "keyword", tmpStr)
                # state = 1
                # tmpStr = ''
                # index += 1
                # continue

            if (state == 35) & (i == 'e'):
                state = 36
                tmpStr += i
                index += 1
                continue
            if (state == 36) & (i == 'g'):
                state = 37
                tmpStr += i
                index += 1
                continue
            if (state == 37) & (i == 'i'):
                state = 38
                tmpStr += i
                index += 1
                continue
            if (state == 38) & (i == 'n'):
                state = 39
                tmpStr += i
            if state == 39:
                # begin
                index += 1
                return twoTuple("关键字begin", tmpStr)
                # printToUI(self, "keyword", tmpStr)
                # state = 1
                # tmpStr = ''
                # index += 1
                # continue

            if (state == 40) & (i == 'h'):
                state = 41
                tmpStr += i
                index += 1
                continue
            if (state == 41) & (i == 'i'):
                state = 42
                tmpStr += i
                index += 1
                continue
            if (state == 42) & (i == 'l'):
                state = 43
                tmpStr += i
                index += 1
                continue
            if (state == 43) & (i == 'e'):
                state = 44
                tmpStr += i
            if state == 44:
                # while
                index += 1
                return twoTuple("关键字while", tmpStr)
                # printToUI(self, "keyword", tmpStr)
                # state = 1
                # tmpStr = ''
                # index += 1
                # continue

            if (state == 45) & (i == 'o'):
                state = 46
                tmpStr += i
            if state == 46:
                # do
                index += 1
                return twoTuple("关键字do", tmpStr)
                # printToUI(self, "keyword", tmpStr)
                # state = 1
                # tmpStr = ''
                # index += 1
                # continue

            if state == 47:
                # 数字
                if i.isdigit():
                    state = 47
                    tmpStr += i
                    index += 1
                    continue
                else:
                    numberList.append(tmpStr)
                    return twoTuple("数字", tmpStr)
                    # printToUI(self, "number", tmpStr)
                    # numberList.append(tmpStr)
                    # state = 1
                    # tmpStr = ''
                    # continue

            # printToUI(self, "未知", i)
            index += 1
            tmpStr += i
            return twoTuple('error', tmpStr)
        # elif i == '#' and state == 1:
        #     return twoTuple('#', '#')
        else:
            return twoTuple('#', '#')
    # self.uiFile.listWidget.addItem('identify table:' + entity.name + ',' + entity.type + ',' + entity.value + ';')
    # tmp = ''
    # for i in identifyList:
    #     tmp = tmp + i.name + ',' + i.type + ',' + i.value + ';'
    # self.uiFile.listWidget.addItem('identify table:' + tmp)
    # tmp = ''
    # for i in numberList:
    #     tmp = tmp + i + ','
    # tmp = tmp[:-1]
    # self.uiFile.listWidget.addItem('const table:' + tmp)
    # utils.printLog(self.uiFile, "\t词法分析结束")
    return None


# 词法分析 ，此词法分析具有简单错误检测与修正，上面的词法分析未于此词法分析合并
def transData(self):
    self.uiFile.listWidget.clear()
    global numberList, identifyList
    state = 1
    index = 0
    tmpStr = ''
    numberList = []
    identifyList = []
    count = len(codeStr)
    while index <= count:
        # for i in codeStr:
        i = codeStr[index]
        if i != '#':
            if i == ' ':
                index += 1
                continue
            if state == 1:
                tmpStr = ''
                if i == ';':
                    state = 4
                    tmpStr += i
                    index += 1
                if i == ',':
                    state = 5
                    tmpStr += i
                    index += 1
                if i == '=':
                    state = 6
                    tmpStr += i
                    index += 1
                    continue
                if i == '<':
                    state = 7
                    tmpStr += i
                    index += 1
                    continue
                if i == '>':
                    state = 8
                    tmpStr += i
                    index += 1
                    continue
                if i == '!':
                    state = 9
                    tmpStr += i
                    index += 1
                    continue
                if i == '+':
                    state = 11
                    tmpStr += i
                    index += 1
                if i == '-':
                    state = 12
                    tmpStr += i
                    index += 1
                if i == '*':
                    state = 13
                    tmpStr += i
                    index += 1
                if i == '/':
                    state = 14
                    tmpStr += i
                    index += 1
                if i == '(':
                    state = 15
                    tmpStr += i
                    index += 1
                if i == ')':
                    state = 16
                    tmpStr += i
                    index += 1
                if i == 'i':
                    state = 21
                    tmpStr += i
                    index += 1
                    continue
                if i == 't':
                    state = 25
                    tmpStr += i
                    index += 1
                    continue
                if i == 'e':
                    state = 29
                    tmpStr += i
                    index += 1
                    continue
                if i == 'b':
                    state = 35
                    tmpStr += i
                    index += 1
                    continue
                if i == 'w':
                    state = 40
                    tmpStr += i
                    index += 1
                    continue
                if i == 'd':
                    state = 45
                    tmpStr += i
                    index += 1
                    continue
                if i.isdigit():
                    # 数字
                    state = 47
                    tmpStr += i
                    index += 1
                    continue
            if (state == 1) & (i == '$'):
                state = 2
                tmpStr += i
                index += 1
                continue
            if state == 2:
                # isalpha 是否是英文字母
                # 此处判定是否是纯英文变量
                state = 3
                tmpStr += i
                index += 1
                continue
            if state == 3:
                if i.isalpha():
                    state = 3
                    tmpStr += i
                    index += 1
                    continue
                elif i.isdigit():
                    state = 3
                    tmpStr += i
                    index += 1
                    continue
                else:
                    # identifier 标识符
                    printToUI(self, "identifier", tmpStr)
                    addTOTable(tmpStr, '', '')
                    state = 1
                    tmpStr = ''
                    continue
            if state == 4:
                # ;号
                printToUI(self, "seperator", tmpStr)
                state = 1
                tmpStr = ''
                continue
            if state == 5:
                # ,号
                printToUI(self, "seperator", tmpStr)
                state = 1
                tmpStr = ''
                continue
            if state == 6:
                # =号
                if i == '=':
                    state = 6
                    tmpStr += i
                    index += 1
                    continue
                else:
                    printToUI(self, "mathOperator", tmpStr)
                    state = 1
                    tmpStr = ''
                    continue
            if state == 7:
                # <号
                if i == '=':
                    state = 7
                    tmpStr += i
                    index += 1
                    continue
                else:
                    printToUI(self, "logicOperator", tmpStr)
                    state = 1
                    tmpStr = ''
                    continue
            if state == 8:
                # >号
                if i == '=':
                    state = 8
                    tmpStr += i
                    index += 1
                    continue
                else:
                    printToUI(self, "logicOperator", tmpStr)
                    state = 1
                    tmpStr = ''
                    continue
            if state == 9:
                # !号
                if i == '=':
                    state = 9
                    tmpStr += i
                    index += 1
                    continue
                else:
                    printToUI(self, "logicOperator", tmpStr)
                    state = 1
                    tmpStr = ''
                    continue
            if state == 11:
                # +号
                printToUI(self, "mathOperator", tmpStr)
                state = 1
                tmpStr = ''
                continue
            if state == 12:
                # -号
                printToUI(self, "mathOperator", tmpStr)
                state = 1
                tmpStr = ''
                continue
            if state == 13:
                # *号
                printToUI(self, "mathOperator", tmpStr)
                state = 1
                tmpStr = ''
                continue
            if state == 14:
                # /号
                printToUI(self, "mathOperator", tmpStr)
                state = 1
                tmpStr = ''
                continue
            if state == 15:
                # (号
                printToUI(self, "mathOperator", tmpStr)
                state = 1
                tmpStr = ''
                continue
            if state == 16:
                # )号
                printToUI(self, "mathOperator", tmpStr)
                state = 1
                tmpStr = ''
                continue

            if (state == 21) & (i == 'n'):
                state = 22
                tmpStr += i
                index += 1
                continue
            if (state == 21) & (i == 'f'):
                state = 24
                tmpStr += i
            if (state == 22) & (i == 't'):
                state = 23
                tmpStr += i
            if state == 23:
                # int
                printToUI(self, "变量说明", tmpStr)
                state = 1
                tmpStr = ''
                index += 1
                continue

            if state == 24:
                # if
                printToUI(self, "keyword", tmpStr)
                state = 1
                tmpStr = ''
                index += 1
                continue

            if (state == 25) & (i == 'h'):
                state = 26
                tmpStr += i
                index += 1
                continue
            if (state == 26) & (i == 'e'):
                state = 27
                tmpStr += i
                index += 1
                continue
            if (state == 27) & (i == 'n'):
                state = 28
                tmpStr += i
            if state == 28:
                # then
                printToUI(self, "keyword", tmpStr)
                state = 1
                tmpStr = ''
                index += 1
                continue

            if (state == 29) & (i == 'l'):
                state = 30
                tmpStr += i
                index += 1
                continue
            if (state == 29) & (i == 'n'):
                state = 33
                tmpStr += i
                index += 1
                continue
            if (state == 30) & (i == 's'):
                state = 31
                tmpStr += i
                index += 1
                continue
            if (state == 31) & (i == 'e'):
                state = 32
                tmpStr += i
            if state == 32:
                # else
                printToUI(self, "keyword", tmpStr)
                state = 1
                tmpStr = ''
                index += 1
                continue

            if (state == 33) & (i == 'd'):
                state = 34
                tmpStr += i
            if state == 34:
                # end
                printToUI(self, "keyword", tmpStr)
                state = 1
                tmpStr = ''
                index += 1
                continue

            if (state == 35) & (i == 'e'):
                state = 36
                tmpStr += i
                index += 1
                continue
            if (state == 36) & (i == 'g'):
                state = 37
                tmpStr += i
                index += 1
                continue
            if (state == 37) & (i == 'i'):
                state = 38
                tmpStr += i
                index += 1
                continue
            if (state == 38) & (i == 'n'):
                state = 39
                tmpStr += i
            if state == 39:
                # begin
                printToUI(self, "keyword", tmpStr)
                state = 1
                tmpStr = ''
                index += 1
                continue

            if (state == 40) & (i == 'h'):
                state = 41
                tmpStr += i
                index += 1
                continue
            if (state == 41) & (i == 'i'):
                state = 42
                tmpStr += i
                index += 1
                continue
            if (state == 42) & (i == 'l'):
                state = 43
                tmpStr += i
                index += 1
                continue
            if (state == 43) & (i == 'e'):
                state = 44
                tmpStr += i
            if state == 44:
                # while
                printToUI(self, "keyword", tmpStr)
                state = 1
                tmpStr = ''
                index += 1
                continue

            if (state == 45) & (i == 'o'):
                state = 46
                tmpStr += i
            if state == 46:
                # do
                printToUI(self, "keyword", tmpStr)
                state = 1
                tmpStr = ''
                index += 1
                continue

            if state == 47:
                # 数字
                if i.isdigit():
                    state = 47
                    tmpStr += i
                    index += 1
                    continue
                else:
                    printToUI(self, "number", tmpStr)
                    numberList.append(tmpStr)
                    state = 1
                    tmpStr = ''
                    continue
            # 修正
            if i == ';':
                printToUI(self, "未知", tmpStr)
                tmpStr = ''
                state = 4
                tmpStr += i
                index += 1
            if i == ',':
                printToUI(self, "未知", tmpStr)
                tmpStr = ''
                state = 5
                tmpStr += i
                index += 1
            if i == '=':
                printToUI(self, "未知", tmpStr)
                tmpStr = ''
                state = 6
                tmpStr += i
                index += 1
                continue
            if i == '<':
                printToUI(self, "未知", tmpStr)
                tmpStr = ''
                state = 7
                tmpStr += i
                index += 1
                continue
            if i == '>':
                printToUI(self, "未知", tmpStr)
                tmpStr = ''
                state = 8
                tmpStr += i
                index += 1
                continue
            if i == '!':
                printToUI(self, "未知", tmpStr)
                tmpStr = ''
                state = 9
                tmpStr += i
                index += 1
                continue
            if i == '+':
                printToUI(self, "未知", tmpStr)
                tmpStr = ''
                state = 11
                tmpStr += i
                index += 1
            if i == '-':
                printToUI(self, "未知", tmpStr)
                tmpStr = ''
                state = 12
                tmpStr += i
                index += 1
            if i == '*':
                printToUI(self, "未知", tmpStr)
                tmpStr = ''
                state = 13
                tmpStr += i
                index += 1
            if i == '/':
                printToUI(self, "未知", tmpStr)
                tmpStr = ''
                state = 14
                tmpStr += i
                index += 1
            if i == '(':
                printToUI(self, "未知", tmpStr)
                tmpStr = ''
                state = 15
                tmpStr += i
                index += 1
            if i == ')':
                printToUI(self, "未知", tmpStr)
                tmpStr = ''
                state = 16
                tmpStr += i
                index += 1
            if i == 'i':
                printToUI(self, "未知", tmpStr)
                tmpStr = ''
                state = 21
                tmpStr += i
                index += 1
                continue
            if i == 't':
                printToUI(self, "未知", tmpStr)
                tmpStr = ''
                state = 25
                tmpStr += i
                index += 1
                continue
            if i == 'e':
                printToUI(self, "未知", tmpStr)
                tmpStr = ''
                state = 29
                tmpStr += i
                index += 1
                continue
            if i == 'b':
                printToUI(self, "未知", tmpStr)
                tmpStr = ''
                state = 35
                tmpStr += i
                index += 1
                continue
            if i == 'w':
                printToUI(self, "未知", tmpStr)
                tmpStr = ''
                state = 40
                tmpStr += i
                index += 1
                continue
            if i == 'd':
                printToUI(self, "未知", tmpStr)
                tmpStr = ''
                state = 45
                tmpStr += i
                index += 1
                continue
            if i == '$':
                printToUI(self, "未知", tmpStr)
                tmpStr = ''
                state = 2
                tmpStr += i
                index += 1
                continue
            index += 1
            tmpStr += i
            state = 1
            printToUI(self, "未知", tmpStr)
        else:
            printToUI(self, "结束符号", '#')
            break
    # self.uiFile.listWidget.addItem('identify table:' + entity.name + ',' + entity.type + ',' + entity.value + ';')
    tmp = ''
    for i in identifyList:
        tmp = tmp + i.name + ',' + i.type + ',' + i.value + ';'
    self.uiFile.listWidget.addItem('identify table: ' + tmp)
    tmp = ''
    for i in numberList:
        tmp = tmp + i + ','
    tmp = tmp[:-1]
    self.uiFile.listWidget.addItem('const table: ' + tmp)


def match(self, type):
    global word
    while word.getType() == 'error':
        # 如何类型是error，即错误单词，循环直到正确
        printToUI2(self, '[词]错误单词: ' + word.toString())
        word = nextInput(self)
    if type != word.getType():
        printToUI2(self, '匹配失败: ' + word.getValue())
        word = nextInput(self)
        while word.getType() == 'error':
            printToUI2(self, '[词]错误单词: ' + word.toString())
            word = nextInput(self)
        printToUI2(self, '[词]识别单词: ' + word.toString())
        return False
    word = nextInput(self)
    while word.getType() == 'error':
        printToUI2(self, '[词]错误单词: ' + word.toString())
        word = nextInput(self)
    printToUI2(self, '[词]识别单词: ' + word.toString())
    return True
    # if type != word.getType():
    #     printToUI2(self, '匹配失败: ' + word.getValue())
    #     word = nextInput(self)
    #     printToUI2(self, '[词]识别单词: ' + word.toString())
    #     return False
    # # else:
    # #     printToUI2(self, '匹配成功')
    # #     word = nextInput(self)
    # #     printToUI2(self, '[词]识别单词: ' + word.toString())
    # #     return True
    # word = nextInput(self)
    # printToUI2(self, '[词]识别单词: ' + word.toString())
    # return True


def parseProgarm(self):
    printToUI2(self, '推导: <程序> →<变量说明部分>;<语句部分>')
    T = parseExplainVars(self)
    if not T:
        utils.printLog(self.uiFile, '\t语法错误：缺少变量申明')
    match(self, "分号")
    parseStatementSection(self)
    # utils.printLog(self.uiFile, "\t语法分析结束")
    return True


def parseExplainVars(self):
    # 变量说明
    printToUI2(self, '推导: <变量说明部分> → int<标识符列表>')
    T = match(self, "int")
    if not T:
        utils.printLog(self.uiFile, '\t语义错误：变量说明部分错误')
        return False
    else:
        parseIdentifierList(self, 'int')
        return True


def parseIdentifierList(self, type):
    # 标识符
    printToUI2(self, '推导: <标识符列表> → <标识符><标识符列表prime>')
    if word.getType() == '标识符':
        updateIdentifyTypeByName(word.getValue(), 'int')
        printToUI2(self, '[翻]更新标识符' + word.getValue() + '为int')
        # 加入标识符重复检查列表
        identifyCheckList.append(word.getValue())
        match(self, "标识符")
    else:
        utils.printLog(self.uiFile, '\t语法错误, 缺少标识符')
    parseIdentifierListPrime(self, type)
    return True


def parseIdentifierListPrime(self, type):
    # 标识符列表
    printToUI2(self, '推导: <标识符列表prime> → ,<标识符><标识符列表prime>|ε')
    if word.getType() == '逗号':
        match(self, "逗号")
        if word.getType() == '标识符':
            isCheck = False  # 默认false，如果已经在identifyCheckList列表里，设为True
            # 在identifyCheckList里面循环检查是否有相同的表示符，有就是重复定义
            for i in identifyCheckList:
                if word.getValue() == i:
                    utils.printLog(self.uiFile, '\t语义错误:标识符 ' + word.getValue() + ' 重复定义')
                    isCheck = True
            if not isCheck:
                # 没有相同的表示符，可以加进去，进入下一个单词识别再检查
                identifyCheckList.append(word.getValue())
            updateIdentifyTypeByName(word.getValue(), 'int')
            printToUI2(self, '[翻]更新标识符' + word.getValue() + '为int')
            match(self, "标识符")
        else:
            utils.printLog(self.uiFile, '\t语义错误, 标识符列表prime翻译失败')
        parseIdentifierListPrime(self, type)
    else:
        pass
    return True


def parseStatementSection(self):
    # 语句部分
    printToUI2(self, '推导: <语句部分> → <语句>;<语句部分prime>')
    parseStatement(self)
    match(self, '分号')
    parseStatementSectionPrime(self)
    return True


def parseStatementSectionPrime(self):
    # 语句部分prime
    if word.getType() == '标识符' or word.getType() == '关键字if':
        printToUI2(self, '推导: <语句部分prime> → <语句>;<语句部分prime>|ε')
        parseStatement(self)
        match(self, '分号')
        parseStatementSectionPrime(self)
    elif word.getType() == '标识符' or word.getType() == '关键字while':
        printToUI2(self, '推导: <语句部分prime> → <语句>;<语句部分prime>|ε')
        parseStatement(self)
        match(self, '分号')
        parseStatementSectionPrime(self)
    else:
        pass
    return True


def parseStatement(self):
    # 语句
    # printToUI2(self, '推导: <语句> → <赋值语句>|<条件语句>|<循环语句>')
    if word.getType() == '标识符':
        printToUI2(self, '推导: <语句> → <赋值语句>')
        parseAssignStatement(self)
    if word.getType() == '关键字if':
        printToUI2(self, '推导: <语句> → <条件语句>')
        parseIfStatement(self)
    if word.getType() == '关键字while':
        printToUI2(self, '推导: <语句> → <循环语句>')
        pareWhileStatement(self)
    return True


def parseAssignStatement(self):
    # 赋值语句
    printToUI2(self, '推导: <赋值语句> → <标识符>=<表达式>')
    identifyname = ''
    if word.getType() == '标识符':
        identifyname = word.getValue()
        printToUI2(self, '[翻]获取赋值语句标识符' + word.getValue())
        match(self, '标识符')
    tmp = match(self, '赋值号')
    # if not tmp:
    #     utils.printLog(self.uiFile, '\t语法错误: 语句错误')
    E = parseExpression(self)
    printToUI2(self, '[翻]输出赋值语句四元式')
    addToMiddleTable('=', E.name, 'null', identifyname)
    printToUI2(self, '[翻]更新标识符' + identifyname + '值为' + E.value)
    updateIdentifyValueByName(identifyname, E.value)
    return True


def parseIfStatement(self):
    # if条件语句
    # <条件语句> → if （<条件>） then <嵌套语句>; else <嵌套语句>
    # <条件语句> → if (<条件>) then <复合语句>; else <复合语句>
    printToUI2(self, '推导: <条件语句> → if （<条件>） then <嵌套语句>; else <嵌套语句>')
    match(self, '关键字if')
    match(self, '左括号')
    E = parseLogicExpression(self)
    match(self, '右括号')
    match(self, '关键字then')
    printToUI2(self, '[翻]输出if语句真出口跳转四元式')
    addToMiddleTable("jnz", E.name, 'null', str(NXQ() + 2))
    falseExit = NXQ()
    printToUI2(self, '[翻]输出if语句假出口跳转四元式')
    addToMiddleTable("j", 'null', 'null', '0')
    exitIndex = 0
    if word.getType() == '关键字begin':
        printToUI2(self, '推导: <嵌套语句> → <复合语句>')
        parseCounpoundStatement(self)
        exitIndex = NXQ()
        addToMiddleTable("j", 'null', 'null', '0')
        printToUI2(self, '[翻]回填if语句假出口地址')
        backPath(falseExit, str(NXQ()))
    else:
        # 语句
        printToUI2(self, '推导: <嵌套语句> → <语句>')
        parseStatement(self)
        exitIndex = NXQ()
        addToMiddleTable("j", 'null', 'null', '0')
        printToUI2(self, '[翻]回填if语句假出口地址')
        backPath(falseExit, str(NXQ()))
    match(self, '分号')
    match(self, '关键字else')
    if word.getType() == '关键字begin':
        printToUI2(self, '推导: <嵌套语句> → <复合语句>')
        parseCounpoundStatement(self)
        printToUI2(self, '[翻]回填if语句出口地址')
        backPath(exitIndex, str(NXQ()))
    else:
        # 语句
        printToUI2(self, '推导: <嵌套语句> → <语句>')
        parseStatement(self)
        printToUI2(self, '[翻]回填if语句出口地址')
        backPath(exitIndex, str(NXQ()))
    return True


def pareWhileStatement(self):
    # while 循环语句
    printToUI2(self, '推导: <循环语句> → while （<条件>） do <嵌套语句>')
    match(self, '关键字while')
    match(self, '左括号')
    number = NXQ()
    E = parseLogicExpression(self)
    match(self, '右括号')
    match(self, '关键字do')
    printToUI2(self, '[翻]输出while语句真出口跳转四元式')
    addToMiddleTable("jnz", E.name, 'null', str(NXQ() + 2))
    falseExit = NXQ()
    printToUI2(self, '[翻]输出while语句假出口跳转四元式')
    addToMiddleTable("j", 'null', 'null', '0')
    exitIndex = 0
    if word.getType() == '关键字begin':
        printToUI2(self, '推导: <嵌套语句> → <复合语句>')
        parseCounpoundStatement(self)
        exitIndex = NXQ()
        addToMiddleTable("j", 'null', 'null', '0')
        backPath(falseExit, str(NXQ()))
        # backPath(exitIndex, number)
    else:
        # 语句
        printToUI2(self, '推导: <嵌套语句> → <语句>')
        parseStatement(self)
        exitIndex = NXQ()
        addToMiddleTable("j", 'null', 'null', '0')
        backPath(falseExit, str(NXQ()))
        # backPath(exitIndex, number)
    printToUI2(self, '[翻]回填while语句出口地址')
    backPath(exitIndex, str(number))
    return True


def parseExpression(self):
    # 表达式
    printToUI2(self, '推导: <表达式> → <项><表达式prime>')
    E = parseItem(self)
    E2 = parseExpressionPrime(self, E)
    return E2


def parseExpressionPrime(self, E):
    # 表达式prime
    # printToUI2(self, '推导: <表达式prime> → + <项><表达式prime>|ε')
    if word.getType() == '加法运算符':
        printToUI2(self, '推导: <表达式prime> → + <项><表达式prime>|ε')
        match(self, '加法运算符')
        E2 = parseItem(self)
        printToUI2(self, '[翻]创建加法运算临时变量')
        T = tempVarTable()
        printToUI2(self, '[翻]输出加法运算四元式')
        addToMiddleTable('+', E.name, E2.name, T.name)
        # T.value = str(int(E.value, 10) + int(E2.value, 10))
        if not E.value:
            utils.printLog(self.uiFile, '\t语义错误：' + E.name + '未赋值')
        if E.value and E2.value:
            T.value = str(int(E.value, 10) + int(E2.value, 10))
        else:
            utils.printLog(self.uiFile, '\t语义错误：' + '项计算失败')
            utils.printLog(self.uiFile, '\t语义错误：' + '表达式计算失败')
        E3 = parseExpressionPrime(self, T)
        return E3
    else:
        return E
    # return E3


def parseItem(self):
    # 项
    printToUI2(self, '推导: <项> → <因子><项prime>|ε')
    E = parseFactor(self)
    E2 = parseItemPrime(self, E)
    if E2:
        return E2
    else:
        return E


def parseItemPrime(self, E):
    # 项
    # printToUI2(self, '推导: <项> → <因子><项prime>')
    # E = identifyTable('')
    # if word.getType() == '标识符':
    #     printToUI2(self, '推导: <项prime> → <标识符>')
    #     E = identifyTable(word.getValue())
    #     E.type = 'int'
    #     match(self, '标识符')
    if word.getType() == '乘法运算符':
        printToUI2(self, '推导: <项prime> → <乘法运算符>')
        match(self, '乘法运算符')
        E2 = parseFactor(self)
        printToUI2(self, '[翻]创建乘法运算临时变量')
        T = tempVarTable()
        printToUI2(self, '[翻]输出乘法四元式')
        addToMiddleTable('*', E.name, E2.name, T.name)
        # if E.value == '':
        #     utils.printLog(self.uiFile, '语义错误：' + E.name + '未赋初值')
        # printToUI2(self, '[语义错误：]' + E.name + '未赋初值')

        # T.value = str(int(E.value, 10) + int(E2.value, 10))
        if E.value and E2.value:
            T.value = str(int(E.value, 10) * int(E2.value, 10))
        else:
            utils.printLog(self.uiFile, '\t语义错误：' + '因子计算失败')
        E3 = parseItemPrime(self, T)
        if E3:
            return E3
        else:
            return T
    # elif word.getType() == '数字':
    #     printToUI2(self, '推导: <项prime> → <数字>')
    #     E = identifyTable(word.getValue())
    #     E.type = 'int'
    #     match(self, '数字')
    elif word.getType() == '左括号':
        printToUI2(self, '推导: <项prime> → <因子><项prime>')
        match(self, '左括号')
        E2 = parseFactor(self)
        E3 = parseItemPrime(self, E2)
        return E3
    # E.type = 'int'
    # else:
    #     parseExpression(self)

    # return True


def parseFactor(self):
    # printToUI2(self, '推导: <因子> → <标识符>|<常量>|(<表达式>)')
    E = identifyTable('')
    if word.getType() == '标识符':
        printToUI2(self, '推导: <因子> → <标识符>')
        E = identifyTable(word.getValue())
        E.value = getIdentifyValueByName(word.getValue())
        match(self, '标识符')
    elif word.getType() == '数字':
        printToUI2(self, '推导: <因子> → <数字>')
        E = identifyTable(word.getValue())
        E.value = word.getValue()
        match(self, '数字')
    elif word.getType() == '左括号':
        printToUI2(self, '推导: <因子> → (<表达式>)')
        match(self, "左括号")
        E = parseExpression(self)
        match(self, "右括号")
    else:
        pass
    return E


def parseLogicExpression(self):
    # 逻辑运算
    printToUI2(self, '推导: <条件> → <表达式><关系运算符><表达式>')
    # match(self, '标识符')
    E = parseExpression(self)
    logicOperator = word.getValue()
    tmp = match(self, '关系运算符')
    if not tmp:
        utils.printLog(self.uiFile, '\t语法错误: 非关系运算符')
    E2 = parseExpression(self)
    # match(self, '数字')
    T = tempVarTable()
    printToUI2(self, '[翻]输出逻辑运算四元式')
    addToMiddleTable(logicOperator, E.name, E2.name, T.name)
    T.type = 'bool'
    R1 = getIdentifyValueByName(E.name)
    R2 = getIdentifyValueByName(E2.name)
    if R1 and R2:
        value1 = int(R1, 10)
        value2 = int(R2, 10)
        if logicOperator == '<':
            if value1 < value2:
                T.value = 'true'
            else:
                T.value = 'false'
        if logicOperator == '>':
            if value1 > value2:
                T.value = 'true'
            else:
                T.value = 'false'
        if logicOperator == '==':
            if value1 == value2:
                T.value = 'true'
            else:
                T.value = 'false'
        if logicOperator == '<=':
            if value1 <= value2:
                T.value = 'true'
            else:
                T.value = 'false'
        if logicOperator == '>=':
            if value1 >= value2:
                T.value = 'true'
            else:
                T.value = 'false'
        if logicOperator == '!=':
            if value1 != value2:
                T.value = 'true'
            else:
                T.value = 'false'
    return T


def parseCounpoundStatement(self):
    # 复合语句
    printToUI2(self, '推导: <复合语句> → begin <语句部分> end')
    match(self, '关键字begin')
    parseStatementSection(self)
    match(self, '关键字end')
    return True


class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        # self.load_ui()
        self.uiFile = self.load_ui()
        self.uiFile.pushButton.clicked.connect(lambda: filePathSelect(self))
        self.uiFile.pushButton_2.clicked.connect(lambda: startWork(self))
        self.uiFile.pushButton_3.clicked.connect(lambda: outPutFile(self))
        self.uiFile.pushButton_4.clicked.connect(lambda: transData(self))
        self.uiFile.listWidget_2.addItem("\t日志输出区域:\n")

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        uiFile = loader.load(ui_file, self)
        ui_file.close()
        return uiFile


if __name__ == "__main__":
    setDefaultPath()
    app = QApplication([])
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
