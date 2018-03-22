#!usr/bin/python
#coding=utf-8

import utils.log.logEvent as log
#测试logEvent
@log.LogEvent("Test")
def testLog_type():
    print("--fucking testing---")

#testing logExcept
@log.LogExcept
@log.LogEvent("Test")
def testLog_error():
    raise IOError,"-----fucking you-----"
testLog_error()