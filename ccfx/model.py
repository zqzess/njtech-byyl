# -*- coding: utf-8 -*-
"""
@Time ： 2022/5/5 18:12
@Auth ： zqzess
@File ：model.py
@IDE ：PyCharm
@Motto：亦余心之所善兮,虽九死其犹未悔
"""
from collections import namedtuple


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
class Entity(object):
    """docstring for Entity"""

    def __init__(self, class_name, columns, **kwargs):
        super(Entity, self).__init__()
        _columns = [i.strip() for i in columns.split(" ") if i.strip()]
        _columns.extend(kwargs.keys())
        columns = list(set(_columns))
        entity = namedtuple(class_name, columns)
        self._entity = entity(**kwargs)

    def __getattribute__(self, key):
        entity = super(Entity, self).__getattribute__("_entity")
        try:
            return super(Entity, self).__getattribute__(key)
        except:
            return getattr(entity, key)

    def __setattr__(self, key, value):
        if key == "_entity":
            super(Entity, self).__setattr__("_entity", value)
            return
        entity = super(Entity, self).__getattribute__("_entity")
        try:
            # setattr(entity, key, value)
            entity.__setattr__(key, value)
        except:
            super(Entity, self).__setattr__(key, value)

# 相当于java的实体类
class fourTuple:
    def __init__(self, operator, operand, operand2, result):
        self.operator = operator
        self.operand = operand
        self.operand2 = operand2
        self.result = result

    def toString(self):
        return '( ' + self.operator + '， ' + self.operand + '， ' + self.operand2 + '， ' + self.result + ' )'
