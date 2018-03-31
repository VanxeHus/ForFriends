#!usr/bin/python
# coding=utf-8
import MySQLdb
from DBUtils.PooledDB import PooledDB
from utils.config import MysqlConfig


class MysqlManager:
    def __init__(self):
        self.mysqlPool = PooledDB(MySQLdb,
                                  # 最大最小连接数量
                                  MysqlConfig.minCache, MysqlConfig.maxCache,
                                  maxconnections=MysqlConfig.maxConnections,
                                  # 阻塞以及数据库名称
                                  blocking=MysqlConfig.blocking, db=MysqlConfig.dbName,
                                  host=MysqlConfig.host, port=MysqlConfig.port,
                                  user=MysqlConfig.user, passwd=MysqlConfig.pwd)

    def getUser(self, userName):
        # 获取用户信息
        conn = self.mysqlPool.connection()
        cur = conn.cursor()
        selcStr = "Select * from user where user=%s"

        resM={}
        if userName:
            cur.execute(selcStr, userName)
            res = cur.fetchone()
            resM["User"]=res[0]
            resM["Pwd"]=res[1]
            resM["Pri"]=res[2]
            resM["Salt"]=res[3]
        cur.close()
        conn.close()
        return resM

    def insertUser(self, params):
        # 插入新用户
        conn = self.mysqlPool.connection()
        cur = conn.cursor()
        instStr = "insert into user(user,password,privilege,salt) values(%s,%s,%s,%s)"
        res = {"res": True, "reason": ""}
        if params:
            try:
                cur.execute(instStr, params)
                conn.commit()
                res["res"]=True
                res["reason"]="insert success"
            except:
                conn.rollback()
                res["res"] = False
                res["reason"] = "insert error"
        else:
            res["res"] = False
            res["reason"] = "params is null"
        cur.close()
        conn.close()
        return res

mysqlManager = MysqlManager()
#获取唯一数据库实例
def GetInstance():
    global mysqlManager
    if mysqlManager:
        return mysqlManager
    else:
        mysqlManager=MysqlManager()
        return mysqlManager


