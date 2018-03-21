#!usr/bin/python
#coding=utf-8

import threading
from Model import SessionManager


def testSession_storage():
    sess= SessionManager.SessionStorage("123456", {"test1": "test1", "test2": "test2"})
    assert sess.values=={"test1":"test1","test2":"test2"}
    assert sess.SessionId()=="123456"
    assert sess.Get("test1")=="test1"
    assert sess.Get("test") is None
    sess.Set("test3","test3")
    sess.Delete("test1")
    assert sess.values=={'test3': 'test3', 'test2': 'test2'}

def testProvider():
    pro= SessionManager.Provider()
    assert pro.Sessions =={}

    assert pro.SessionRead("123456") is None
    pro.SessionInit("123456",{"test1":"test1","test2":"test2"})
    assert pro.SessionRead("123456").values !={'test1': 'test1', 'test2': 'test2'}


    pro.SessionDestroy("123456")
    pro.SessionDestroy("123456")
    assert pro.Sessions =={}

def testManager():
    manager= SessionManager.manager
    manager.SessionStart({'test1': 'test1', 'test2': 'test2'})
    manager.SessionStart({'test1': 'test1', 'test2': 'test2'})
    manager.SessionStart({'test1': 'test1', 'test2': 'test2'})
    threading._start_new_thread(manager.TD())