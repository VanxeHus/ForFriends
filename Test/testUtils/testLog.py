#!usr/bin/python
#coding=utf-8

import utils.log.logEvent as log
#测试logEvent
@log.LogEvent("Test")
def testLog_type():
    print("--fucking testing---")
testLog_type()