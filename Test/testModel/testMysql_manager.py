#!usr/bin/python
#conding=utf-8

from Model.MysqlManager import mysqlManager
from Model.MysqlManager import GetInstance

def testGet_user():
    assert ('test','test','test')==mysqlManager.getUser("test")
    assert None==mysqlManager.getUser("VanxeHus")
def testInsert_user():
    pass
def testSingle_ton():
    assert mysqlManager is GetInstance()
