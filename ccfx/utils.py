# -*- coding: utf-8 -*-
"""
@Time ： 2022/4/10 19:46
@Auth ： zqzess
@File ：utils.py
@IDE ：PyCharm
@Motto：亦余心之所善兮,虽九死其犹未悔
"""
from PySide6.QtWidgets import QMessageBox
import os
import time


# 获取当前登录的系统用户
def get_current_user():
    try:
        # pwd is unix only
        import pwd
        return pwd.getpwuid(os.getuid())[0]
    except ImportError as e:
        import getpass
        return getpass.getuser()


# 获取当前登录的系统用户组
def get_default_group_for_user(user):
    import grp
    import pwd
    group = None
    try:
        gid = pwd.getpwnam(user)[3]
        groups = grp.getgrgid(gid)[0]
    except KeyError as e:
        print('Failed to find primary group from user %s', user)
        return group


# 弹窗
def show_errorMessage(title, msg):
    msg_box = QMessageBox(QMessageBox.Critical, title, msg, QMessageBox.Yes)
    msg_box.exec_()


def show_Message(title, msg):
    msg_box = QMessageBox(QMessageBox.Information, title, msg, QMessageBox.Yes)
    msg_box.exec_()


def show_warnMessage(title, msg):
    msg_box = QMessageBox(QMessageBox.Warning, title, msg, QMessageBox.Yes)
    msg_box.exec_()


def show_aboutMessage(title, msg):
    msg_box = QMessageBox(QMessageBox.About, title, msg, QMessageBox.Yes)
    msg_box.exec_()


# 获取文件名
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        # 备注root返回当前目录路径；dirs返回当前路径下所有子目录；files返回当前路径下所有非目录子文件
        # print(files)
        return root, dirs, files


# 输出栏输出操作日志
def printLog(self, msg):
    i = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    self.listWidget_2.addItem(str(i) + msg)
