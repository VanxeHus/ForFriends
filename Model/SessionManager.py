#!usr/bin/python
#coding=utf-8
import threading

import binascii
import os

import schedule
import time
from utils.config import SessionConfig
#session管理器
class Manager:
    def __init__(self, provider, time):
        self.lock = threading.Lock()
        self.provider = provider
        self.time = time

    # 生成uuid
    def __sessionId(self):
        return binascii.b2a_base64(os.urandom(24))[:-1]

    # 创建或返回一个存在的session
    def SessionStart(self,values,sid=None):
        if self.lock.acquire():
            if not sid:
                sid = self.__sessionId()
                sess = self.provider.SessionInit(sid,values)
            else:
                sess = self.provider.SessionRead(sid)
            self.lock.release()
        else:
            return
        return sess

    # 销毁session
    def SessionDestroy(self, sid):
        if self.lock.acquire():
            if not sid:
                self.provider.SessionDestroy(sid)
            self.lock.release()
        else:
            return
        return

    # 定时器,定时销毁长期不用的session
    def TD(self):
        schedule.every(self.time).seconds.do(test)
        schedule.every(self.time).seconds.do(self.lock.acquire)
        schedule.every(self.time).seconds.do(test)
        schedule.every(self.time).seconds.do(self.provider.TD, self.time)
        schedule.every(self.time).seconds.do(self.lock.release)
        while True:
            schedule.run_pending()
# 内存session结构
class SessionStorage:
    #新的session
    def __init__(self,sid,values):
        self.values=values
        self.Set("time",time.time())
        self.sid=sid
    def SessionId(self):
        return self.sid

    def Set(self, key, value):
        self.values[key] = value
        return

    def Get(self, key):
        if self.values.has_key(key):
            return self.values[key]
        return

    def Delete(self, key):
        del self.values[key]
        return
# 内存provider
class Provider:
    def __init__(self):
        self.lock = threading.Lock()
        self.Sessions = {}
    #创建一个新的session
    def SessionInit(self, sid,values):
        sess=None
        if self.lock.acquire():
            self.Sessions[sid] = SessionStorage(sid,values)
            print sid+" created"
            sess=self.Sessions[sid]
            self.lock.release()
        return sess
    #从dict里面读取一个session
    def SessionRead(self, sid):
        sess=None
        if self.lock.acquire():
            if self.Sessions.has_key(sid):
                sess = self.Sessions[sid]
            self.lock.release()
        return sess
    #从session里面销毁session
    #用于退出登录
    def SessionDestroy(self, sid):
        if self.lock.acquire():
            if self.Sessions.has_key(sid):
                del self.Sessions[sid]
            self.lock.release()
    #定时器,定时销毁长期不用的session
    def TD(self, maxtime):
        if self.lock.acquire():
            for key in list(self.Sessions):
                if self.Sessions[key].values["time"] + maxtime < time.time():
                    print key+" deleted"
                    self.Sessions.pop(key)
            self.lock.release()
        return

def test():
    print "test"
memoryProvider=Provider()
manager=Manager(memoryProvider,SessionConfig.maxTime)
def GetInstance():
    #获取全局唯一的manager
    global manager
    global memoryProvider
    if manager:
        return manager
    if memoryProvider:
        pass
    else:
        memoryProvider = Provider()
    manager = Manager(memoryProvider, SessionConfig.maxTime)
    return manager