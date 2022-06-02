# -*- coding: utf-8 -*-
"""
@Time ： 2022/4/25 12:27
@Auth ： zqzess
@File ：widget2.py
@IDE ：PyCharm
@Motto：亦余心之所善兮,虽九死其犹未悔
@desc : Tkinter图形框架
"""
import os
import platform
import tkinter
from tkinter import Tk, Button, W, filedialog, END, RIGHT, Y, BOTTOM, HORIZONTAL, X, YES, BOTH, NONE

rootPath = '/'  # 初始路径
directory = ''  # 输入路径
outFileName = 'out'  # 输出文件名
codeStr = ''  # 保存从txt读取的字符串
b1 = None  # 按钮
b2 = None  # 按钮
b3 = None  # 按钮
listbox = None  # 列表控件
text2 = None  # 文本控件
numberList = []  # 存放源代码里所有数字的列表
identifyList = []  # 存放标识符的列表
index = 0  # 自动机的标号
word = None  # 下一个识别的单词
middleTable = []  # 中间代码（四元式）列表
table = ['']  # 四元式result列表
identifyCheckList = []  # 用于语义分析：重复定义，存放表示符


# 相当于java的实体类
class twoTuple:
    def __init__(self, ctype, value):
        self.ctype = ctype
        self.value = value

    def getType(self):
        return self.ctype

    def setType(self, ctype):
        self.ctype = ctype

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

    def toString(self):
        return '( ' + self.ctype + '， ' + self.value + ' )'


# 相当于java的实体类
class identifyClass:
    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getType(self):
        return self.type

    def setType(self, type):
        self.type = type

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value


# 相当于java的实体类
class fourTuple:
    def __init__(self, operator, operand, operand2, result):
        self.operator = operator
        self.operand = operand
        self.operand2 = operand2
        self.result = result

    def toString(self):
        return '( ' + self.operator + '， ' + self.operand + '， ' + self.operand2 + '， ' + self.result + ' )'


def addTOTable(name, type, value):
    identify = identifyClass(name, type, value)
    tmp = False
    if len(identifyList) == 0:
        identifyList.append(identify)
    else:
        # 去重，防止重复添加
        for i in identifyList:
            if i.getName() == name:
                tmp = True
        if not tmp:
            identifyList.append(identify)
    # identifyList.append(identify)


def identifyTable(name):
    identify = identifyClass(name, '', '')
    identify.setName(name)
    return identify


# 添加四元式至四元式列表
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


# 打印至日志区
def printLog(msg):
    text2.insert(END, '\n' + msg)


def updateIdentifyTypeByName(name, type):
    for i in identifyList:
        if i.getName() == name:
            i.setType(type)
            break


def updateIdentifyValueByName(name, value):
    for i in identifyList:
        if i.getName() == name:
            i.setValue(value)


def getIdentifyValueByName(name):
    for i in identifyList:
        if i.getName() == name:
            return i.getValue()


# 打印至屏幕
def printToUI(ctype, name):
    listbox.insert(END, "(" + ctype + " , " + name + ")")


def printToUI2(msg):
    listbox.insert(END, msg)


# 获取当前登录的系统用户
def get_current_user():
    try:
        # pwd is unix only
        import pwd
        return pwd.getpwuid(os.getuid())[0]
    except ImportError as e:
        import getpass
        return getpass.getuser()


# 设置初始文件夹路径
def setDefaultPath():
    global rootPath
    sysstr = platform.system()
    if sysstr == 'Windows':
        rootPath = 'C:/'
    elif sysstr == "Linux":
        rootPath = '/'
    elif sysstr == "Darwin":
        userName = get_current_user()
        rootPath = '/Users/' + userName


# 选择文件路径
def filePathSelect():
    global directory
    root = tkinter.Tk()
    root.withdraw()
    directory = filedialog.askopenfilename(filetypes=[('TXT', 'txt')])
    if directory:
        readDataFromTXT()
    else:
        printLog('没有选择文件')


# 从txt读取数据
def readDataFromTXT():
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
        text2.insert(END, "\n")
        text2.insert(END, "\n代码块")
        text2.insert(END, "\n******************\n")
        text2.insert(END, codeStr + "\n******************\n")


# 输出文件
def outPutFile():
    outPutPath = filedialog.askdirectory()
    if outPutPath:
        outFilePath = str(outPutPath) + '/' + outFileName + '.txt'
        if os.path.exists(outFilePath):
            printLog('存在同名输出文件，将执行删除操作!')
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
            printLog("输出完成!")
    else:
        printLog("未选择输出文件路径!")
        return 0


# 启动入口
def startWork():
    global word, codeStr, numberList, identifyList, index, middleTable, table, identifyCheckList

    middleTable.clear()
    numberList = []
    identifyList = []
    index = 0
    middleTable = []
    table = ['']
    identifyCheckList = []
    listbox.delete(0, END)  # UI控件 列表清空

    if codeStr:
        word = nextInput()
        printToUI2('[词]识别单词: ' + word.toString())
        parseProgarm()
        # # #
        tmp = ''
        for i in identifyList:
            tmp = tmp + i.name + ',' + i.type + ',' + i.value + ';'
        listbox.insert(END, 'identify table: ' + tmp)
        tmp = ''
        for i in numberList:
            tmp = tmp + i + ','
        tmp = tmp[:-1]
        listbox.insert(END, 'const table: ' + tmp)
        printToUI2('\n')
        num = 0
        for i in middleTable:
            printToUI2('(' + str(num) + ')' + ' ' + i.toString())
            num += 1
        printLog("程序执行完成!!!")
    else:
        printLog("输入的源代码为空!!!")


# 词法分析
def nextInput():
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
            if state == 4:
                # ;号
                return twoTuple("分号", tmpStr)
            if state == 5:
                # ,号
                return twoTuple("逗号", tmpStr)
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
            if state == 7:
                # <号
                if i == '=':
                    state = 7
                    tmpStr += i
                    index += 1
                    continue
                else:
                    return twoTuple("关系运算符", tmpStr)
            if state == 8:
                # >号
                if i == '=':
                    state = 8
                    tmpStr += i
                    index += 1
                    continue
                else:
                    return twoTuple("关系运算符", tmpStr)
            if state == 9:
                # !号
                if i == '=':
                    state = 9
                    tmpStr += i
                    index += 1
                    continue
                else:
                    return twoTuple("关系运算符", tmpStr)
            if state == 11:
                # +号
                return twoTuple("加法运算符", tmpStr)
            if state == 12:
                # -号
                return twoTuple("减法运算符", tmpStr)
            if state == 13:
                # *号
                return twoTuple("乘法运算符", tmpStr)
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

            if (state == 33) & (i == 'd'):
                state = 34
                tmpStr += i
            if state == 34:
                # end
                index += 1
                return twoTuple("关键字end", tmpStr)

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

            if (state == 45) & (i == 'o'):
                state = 46
                tmpStr += i
            if state == 46:
                # do
                index += 1
                return twoTuple("关键字do", tmpStr)

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

            index += 1
            return twoTuple('error', tmpStr)
        else:
            return twoTuple('#', '#')
    return None


# 词法分析 ，此词法分析具有简单错误检测与修正，上面的词法分析未于此词法分析合并
def transData():
    listbox.delete(0, END)  # 清空
    global numberList, identifyList  # 使用最上面申明的全局变量
    state = 1
    index = 0  # 此处index为局部变量,nextInput使用的是最顶层申明的全局变量，此处同名不太合法，但是可以使用
    # 此语法分析与上面的不是同一个，是独立的，所以index需要局部变量
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
                    printToUI("identifier", tmpStr)
                    addTOTable(tmpStr, '', '')
                    state = 1
                    tmpStr = ''
                    continue
            if state == 4:
                # ;号
                printToUI("seperator", tmpStr)
                state = 1
                tmpStr = ''
                continue
            if state == 5:
                # ,号
                printToUI("seperator", tmpStr)
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
                    printToUI("mathOperator", tmpStr)
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
                    printToUI("logicOperator", tmpStr)
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
                    printToUI("logicOperator", tmpStr)
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
                    printToUI("logicOperator", tmpStr)
                    state = 1
                    tmpStr = ''
                    continue
            if state == 11:
                # +号
                printToUI("mathOperator", tmpStr)
                state = 1
                tmpStr = ''
                continue
            if state == 12:
                # -号
                printToUI("mathOperator", tmpStr)
                state = 1
                tmpStr = ''
                continue
            if state == 13:
                # *号
                printToUI("mathOperator", tmpStr)
                state = 1
                tmpStr = ''
                continue
            if state == 14:
                # /号
                printToUI("mathOperator", tmpStr)
                state = 1
                tmpStr = ''
                continue
            if state == 15:
                # (号
                printToUI("mathOperator", tmpStr)
                state = 1
                tmpStr = ''
                continue
            if state == 16:
                # )号
                printToUI("mathOperator", tmpStr)
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
                printToUI("变量说明", tmpStr)
                state = 1
                tmpStr = ''
                index += 1
                continue

            if state == 24:
                # if
                printToUI("keyword", tmpStr)
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
                printToUI("keyword", tmpStr)
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
                printToUI("keyword", tmpStr)
                state = 1
                tmpStr = ''
                index += 1
                continue

            if (state == 33) & (i == 'd'):
                state = 34
                tmpStr += i
            if state == 34:
                # end
                printToUI("keyword", tmpStr)
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
                printToUI("keyword", tmpStr)
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
                printToUI("keyword", tmpStr)
                state = 1
                tmpStr = ''
                index += 1
                continue

            if (state == 45) & (i == 'o'):
                state = 46
                tmpStr += i
            if state == 46:
                # do
                printToUI("keyword", tmpStr)
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
                    printToUI("number", tmpStr)
                    numberList.append(tmpStr)
                    state = 1
                    tmpStr = ''
                    continue
            # 修正
            if i == ';':
                printToUI("未知", tmpStr)
                tmpStr = ''
                state = 4
                tmpStr += i
                index += 1
            if i == ',':
                printToUI("未知", tmpStr)
                tmpStr = ''
                state = 5
                tmpStr += i
                index += 1
            if i == '=':
                printToUI("未知", tmpStr)
                tmpStr = ''
                state = 6
                tmpStr += i
                index += 1
                continue
            if i == '<':
                printToUI("未知", tmpStr)
                tmpStr = ''
                state = 7
                tmpStr += i
                index += 1
                continue
            if i == '>':
                printToUI("未知", tmpStr)
                tmpStr = ''
                state = 8
                tmpStr += i
                index += 1
                continue
            if i == '!':
                printToUI("未知", tmpStr)
                tmpStr = ''
                state = 9
                tmpStr += i
                index += 1
                continue
            if i == '+':
                printToUI("未知", tmpStr)
                tmpStr = ''
                state = 11
                tmpStr += i
                index += 1
            if i == '-':
                printToUI("未知", tmpStr)
                tmpStr = ''
                state = 12
                tmpStr += i
                index += 1
            if i == '*':
                printToUI("未知", tmpStr)
                tmpStr = ''
                state = 13
                tmpStr += i
                index += 1
            if i == '/':
                printToUI("未知", tmpStr)
                tmpStr = ''
                state = 14
                tmpStr += i
                index += 1
            if i == '(':
                printToUI("未知", tmpStr)
                tmpStr = ''
                state = 15
                tmpStr += i
                index += 1
            if i == ')':
                printToUI("未知", tmpStr)
                tmpStr = ''
                state = 16
                tmpStr += i
                index += 1
            if i == 'i':
                printToUI("未知", tmpStr)
                tmpStr = ''
                state = 21
                tmpStr += i
                index += 1
                continue
            if i == 't':
                printToUI("未知", tmpStr)
                tmpStr = ''
                state = 25
                tmpStr += i
                index += 1
                continue
            if i == 'e':
                printToUI("未知", tmpStr)
                tmpStr = ''
                state = 29
                tmpStr += i
                index += 1
                continue
            if i == 'b':
                printToUI("未知", tmpStr)
                tmpStr = ''
                state = 35
                tmpStr += i
                index += 1
                continue
            if i == 'w':
                printToUI("未知", tmpStr)
                tmpStr = ''
                state = 40
                tmpStr += i
                index += 1
                continue
            if i == 'd':
                printToUI("未知", tmpStr)
                tmpStr = ''
                state = 45
                tmpStr += i
                index += 1
                continue
            if i == '$':
                printToUI("未知", tmpStr)
                tmpStr = ''
                state = 2
                tmpStr += i
                index += 1
                continue
            index += 1
            tmpStr += i
            state = 1
            printToUI("未知", tmpStr)
        else:
            printToUI("结束符号", '#')
            break
    # self.uiFile.listWidget.addItem('identify table:' + entity.name + ',' + entity.type + ',' + entity.value + ';')
    tmp = ''
    for i in identifyList:
        tmp = tmp + i.name + ',' + i.type + ',' + i.value + ';'
    listbox.insert(END, 'identify table: ' + tmp)
    tmp = ''
    for i in numberList:
        tmp = tmp + i + ','
    tmp = tmp[:-1]
    listbox.insert(END, 'const table: ' + tmp)


def match(type):
    # isMatch = True
    global word
    if type != word.getType():
        printToUI2('匹配失败: ' + word.getValue())
        word = nextInput()
        printToUI2('[词]识别单词: ' + word.toString())
        return False
    word = nextInput()
    printToUI2('[词]识别单词: ' + word.toString())
    return True


def parseProgarm():
    printToUI2('推导: <程序> →<变量说明部分>;<语句部分>')
    T = parseExplainVars()
    if not T:
        printLog('语法错误：缺少变量申明')
    match("分号")
    parseStatementSection()
    return True


def parseExplainVars():
    # 变量说明
    printToUI2('推导: <变量说明部分> → int<标识符列表>')
    T = match("int")
    if not T:
        # printLog('语义错误：变量说明部分错误')
        return False
    else:
        parseIdentifierList('int')
        return True


def parseIdentifierList(type):
    # 标识符
    printToUI2('推导: <标识符列表> → <标识符><标识符列表prime>')
    if word.getType() == '标识符':
        updateIdentifyTypeByName(word.getValue(), 'int')
        printToUI2('[翻]更新标识符' + word.getValue() + '为int')
        # 加入标识符重复检查列表
        identifyCheckList.append(word.getValue())
        match("标识符")
    else:
        printLog('语法错误, 缺少标识符')
    parseIdentifierListPrime(type)
    return True


def parseIdentifierListPrime(type):
    # 标识符列表
    printToUI2('推导: <标识符列表prime> → ,<标识符><标识符列表prime>|ε')
    if word.getType() == '逗号':
        match("逗号")
        if word.getType() == '标识符':
            isCheck = False  # 默认false，如果已经在identifyCheckList列表里，设为True
            # 在identifyCheckList里面循环检查是否有相同的表示符，有就是重复定义
            for i in identifyCheckList:
                if word.getValue() == i:
                    printLog('语义错误:标识符 ' + word.getValue() + ' 重复定义')
                    isCheck = True
            if not isCheck:
                # 没有相同的表示符，可以加进去，进入下一个单词识别再检查
                identifyCheckList.append(word.getValue())
            updateIdentifyTypeByName(word.getValue(), 'int')
            printToUI2('[翻]更新标识符' + word.getValue() + '为int')
            match("标识符")
        else:
            printLog('语法错误：缺少标识符')
            printLog('语义错误, 标识符列表prime翻译失败')
        parseIdentifierListPrime(type)
    else:
        pass
    return True


def parseStatementSection():
    # 语句部分
    printToUI2('推导: <语句部分> → <语句>;<语句部分prime>')
    parseStatement()
    match('分号')
    parseStatementSectionPrime()
    return True


def parseStatementSectionPrime():
    # 语句部分prime
    if word.getType() == '标识符' or word.getType() == '关键字if':
        printToUI2('推导: <语句部分prime> → <语句>;<语句部分prime>|ε')
        parseStatement()
        match('分号')
        parseStatementSectionPrime()
    elif word.getType() == '标识符' or word.getType() == '关键字while':
        printToUI2('推导: <语句部分prime> → <语句>;<语句部分prime>|ε')
        parseStatement()
        match('分号')
        parseStatementSectionPrime()
    else:
        pass
    return True


def parseStatement():
    # 语句
    # printToUI2('推导: <语句> → <赋值语句>|<条件语句>|<循环语句>')
    if word.getType() == '标识符':
        printToUI2('推导: <语句> → <赋值语句>')
        parseAssignStatement()
    if word.getType() == '关键字if':
        printToUI2('推导: <语句> → <条件语句>')
        parseIfStatement()
    if word.getType() == '关键字while':
        printToUI2('推导: <语句> → <循环语句>')
        pareWhileStatement()
    return True


def parseAssignStatement():
    # 赋值语句
    printToUI2('推导: <赋值语句> → <标识符>=<表达式>')
    identifyname = ''
    if word.getType() == '标识符':
        identifyname = word.getValue()
        printToUI2('[翻]获取赋值语句标识符' + word.getValue())
        match('标识符')
    tmp = match('赋值号')
    # if not tmp:
    #     printLog('语法错误: 语句错误')
    E = parseExpression()
    printToUI2('[翻]输出赋值语句四元式')
    addToMiddleTable('=', E.name, 'null', identifyname)
    printToUI2('[翻]更新标识符' + identifyname + '值为' + E.value)
    updateIdentifyValueByName(identifyname, E.value)
    return True


def parseIfStatement():
    # if条件语句
    # <条件语句> → if （<条件>） then <嵌套语句>; else <嵌套语句>
    # <条件语句> → if (<条件>) then <复合语句>; else <复合语句>
    printToUI2('推导: <条件语句> → if （<条件>） then <嵌套语句>; else <嵌套语句>')
    match('关键字if')
    match('左括号')
    E = parseLogicExpression()
    match('右括号')
    match('关键字then')
    printToUI2('[翻]输出if语句真出口跳转四元式')
    addToMiddleTable("jnz", E.name, 'null', str(NXQ() + 2))
    falseExit = NXQ()
    printToUI2('[翻]输出if语句假出口跳转四元式')
    addToMiddleTable("j", 'null', 'null', '0')
    exitIndex = 0
    if word.getType() == '关键字begin':
        printToUI2('推导: <嵌套语句> → <复合语句>')
        parseCounpoundStatement()
        exitIndex = NXQ()
        addToMiddleTable("j", 'null', 'null', '0')
        printToUI2('[翻]回填if语句假出口地址')
        backPath(falseExit, str(NXQ()))
    else:
        # 语句
        printToUI2('推导: <嵌套语句> → <语句>')
        parseStatement()
        exitIndex = NXQ()
        addToMiddleTable("j", 'null', 'null', '0')
        printToUI2('[翻]回填if语句假出口地址')
        backPath(falseExit, str(NXQ()))
    match('分号')
    match('关键字else')
    if word.getType() == '关键字begin':
        printToUI2('推导: <嵌套语句> → <复合语句>')
        parseCounpoundStatement()
        printToUI2('[翻]回填if语句出口地址')
        backPath(exitIndex, str(NXQ()))
    else:
        # 语句
        printToUI2('推导: <嵌套语句> → <语句>')
        parseStatement()
        printToUI2('[翻]回填if语句出口地址')
        backPath(exitIndex, str(NXQ()))
    return True


def pareWhileStatement():
    # while 循环语句
    printToUI2('推导: <循环语句> → while （<条件>） do <嵌套语句>')
    match('关键字while')
    match('左括号')
    number = NXQ()
    E = parseLogicExpression()
    match('右括号')
    match('关键字do')
    printToUI2('[翻]输出while语句真出口跳转四元式')
    addToMiddleTable("jnz", E.name, 'null', str(NXQ() + 2))
    falseExit = NXQ()
    printToUI2('[翻]输出while语句假出口跳转四元式')
    addToMiddleTable("j", 'null', 'null', '0')
    exitIndex = 0
    if word.getType() == '关键字begin':
        printToUI2('推导: <嵌套语句> → <复合语句>')
        parseCounpoundStatement()
        exitIndex = NXQ()
        addToMiddleTable("j", 'null', 'null', '0')
        backPath(falseExit, str(NXQ()))
        # backPath(exitIndex, number)
    else:
        # 语句
        printToUI2('推导: <嵌套语句> → <语句>')
        parseStatement()
        exitIndex = NXQ()
        addToMiddleTable("j", 'null', 'null', '0')
        backPath(falseExit, str(NXQ()))
        # backPath(exitIndex, number)
    printToUI2('[翻]回填while语句出口地址')
    backPath(exitIndex, str(number))
    return True


def parseExpression():
    # 表达式
    printToUI2('推导: <表达式> → <项><表达式prime>')
    E = parseItem()
    E2 = parseExpressionPrime(E)
    return E2


def parseExpressionPrime(E):
    # 表达式prime
    # printToUI2('推导: <表达式prime> → + <项><表达式prime>|ε')
    if word.getType() == '加法运算符':
        printToUI2('推导: <表达式prime> → + <项><表达式prime>|ε')
        match('加法运算符')
        E2 = parseItem()
        printToUI2('[翻]创建加法运算临时变量')
        T = tempVarTable()
        printToUI2('[翻]输出加法运算四元式')
        addToMiddleTable('+', E.name, E2.name, T.name)
        # T.value = str(int(E.value, 10) + int(E2.value, 10))
        if not E.value:
            printLog('语义错误：' + E.name + '未赋值')
        if E.value and E2.value:
            T.value = str(int(E.value, 10) + int(E2.value, 10))
        else:
            printLog('语义错误：' + '项计算失败')
            printLog('语义错误：' + '表达式计算失败')
        E3 = parseExpressionPrime(T)
        return E3
    else:
        return E
    # return E3


def parseItem():
    # 项
    printToUI2('推导: <项> → <因子><项prime>|ε')
    E = parseFactor()
    E2 = parseItemPrime(E)
    if E2:
        return E2
    else:
        return E


def parseItemPrime(E):
    # 项
    # printToUI2('推导: <项> → <因子><项prime>')
    # E = identifyTable('')
    # if word.getType() == '标识符':
    #     printToUI2('推导: <项prime> → <标识符>')
    #     E = identifyTable(word.getValue())
    #     E.type = 'int'
    #     match('标识符')
    if word.getType() == '乘法运算符':
        printToUI2('推导: <项prime> → <乘法运算符>')
        match('乘法运算符')
        E2 = parseFactor()
        printToUI2('[翻]创建乘法运算临时变量')
        T = tempVarTable()
        printToUI2('[翻]输出乘法四元式')
        addToMiddleTable('*', E.name, E2.name, T.name)
        # if E.value == '':
        #     printLog('语义错误：' + E.name + '未赋初值')
        # printToUI2('[语义错误：]' + E.name + '未赋初值')

        # T.value = str(int(E.value, 10) + int(E2.value, 10))
        if E.value and E2.value:
            T.value = str(int(E.value, 10) * int(E2.value, 10))
        else:
            printLog('语义错误：' + '因子计算失败')
        E3 = parseItemPrime(T)
        if E3:
            return E3
        else:
            return T
    # elif word.getType() == '数字':
    #     printToUI2('推导: <项prime> → <数字>')
    #     E = identifyTable(word.getValue())
    #     E.type = 'int'
    #     match('数字')
    elif word.getType() == '左括号':
        printToUI2('推导: <项prime> → <因子><项prime>')
        match('左括号')
        E2 = parseFactor()
        E3 = parseItemPrime(E2)
        return E3
    # E.type = 'int'
    # else:
    #     parseExpression()

    # return True


def parseFactor():
    # printToUI2('推导: <因子> → <标识符>|<常量>|(<表达式>)')
    E = identifyTable('')
    if word.getType() == '标识符':
        printToUI2('推导: <因子> → <标识符>')
        E = identifyTable(word.getValue())
        E.value = getIdentifyValueByName(word.getValue())
        match('标识符')
    elif word.getType() == '数字':
        printToUI2('推导: <因子> → <数字>')
        E = identifyTable(word.getValue())
        E.value = word.getValue()
        match('数字')
    elif word.getType() == '左括号':
        printToUI2('推导: <因子> → (<表达式>)')
        match("左括号")
        E = parseExpression()
        match("右括号")
    else:
        pass
    return E


def parseLogicExpression():
    # 逻辑运算
    printToUI2('推导: <条件> → <表达式><关系运算符><表达式>')
    # match('标识符')
    E = parseExpression()
    logicOperator = word.getValue()
    tmp = match('关系运算符')
    if not tmp:
        printLog('语法错误: 非关系运算符')
    E2 = parseExpression()
    # match('数字')
    T = tempVarTable()
    printToUI2('[翻]输出逻辑运算四元式')
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


def parseCounpoundStatement():
    # 复合语句
    printToUI2('推导: <复合语句> → begin <语句部分> end')
    match('关键字begin')
    parseStatementSection()
    match('关键字end')
    return True


# 初始化UI
def setUI():
    global b1, b2, b3, listbox, text2
    # 初始化Tk()m
    root = Tk()
    # 设置标题
    root.title('Python GUI Learning')
    # 设置窗口大小
    width = 1000
    height = 700
    # 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(alignstr)
    # 设置窗口是否可变长、宽，True：可变，False：不可变
    root.resizable(width=False, height=True)

    b1 = Button(root, text='选择文件', command=filePathSelect, width=10, height=3)
    b1.grid(row=0, column=2, sticky=W, padx=5, pady=5)

    b2 = Button(root, text='运行', command=startWork, width=10, height=3)
    b2.grid(row=1, column=2, sticky=W, padx=5, pady=5)

    b3 = Button(root, text='输出文件', command=outPutFile, width=10, height=3)
    b3.grid(row=2, column=2, sticky=W, padx=5, pady=5)

    fm = tkinter.Frame(root, width=20, height=20)
    fm.grid(row=0, column=0, sticky=W, padx=10, pady=10)
    # 滚动条
    scrollbar_y = tkinter.Scrollbar(fm)
    scrollbar_y.pack(side=RIGHT, fill=Y)
    scrollbar_x = tkinter.Scrollbar(fm, orient=HORIZONTAL)
    scrollbar_x.pack(side=BOTTOM, fill=X)
    # listbox显示区
    listbox = tkinter.Listbox(fm, width=30, height=20, yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    listbox.pack(expand=YES, fill=BOTH)
    # 设置text随滚动条滚动刷新
    scrollbar_x.config(command=listbox.xview)
    scrollbar_y.config(command=listbox.yview)
    # 容器
    fm2 = tkinter.Frame(root, width=50, height=15)
    fm2.grid(row=2, column=0, sticky=W, padx=10, pady=10)
    # 滚动条
    scrollbar_y = tkinter.Scrollbar(fm2)
    scrollbar_y.pack(side=RIGHT, fill=Y)
    scrollbar_x = tkinter.Scrollbar(fm2, orient=HORIZONTAL)
    scrollbar_x.pack(side=BOTTOM, fill=X)
    # text显示区
    text2 = tkinter.Text(fm2, width=50, height=15, yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set,
                         wrap=NONE)
    text2.pack(expand=YES, fill=BOTH)
    # 设置text随滚动条滚动刷新
    scrollbar_x.config(command=text2.xview)
    scrollbar_y.config(command=text2.yview)
    # 进入消息循环
    root.mainloop()


if __name__ == '__main__':
    setDefaultPath()
    setUI()
