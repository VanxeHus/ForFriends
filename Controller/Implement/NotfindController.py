#!usr/bin/python
#coding=utf-8
import struct
from utils.log import logEvent
class NotfindController:
    def __init__(self):
        pass
    #404
    @logEvent.LogEvent("NotfindHandle")
    def Handle(self,sck,addr,data):
        resCode="404\t\n"
        resReason="instruction wrong\t\n"

        headerLen=resCode.__len__()+resReason.__len__()
        headerPack=struct.pack(">I4s",headerLen,"404")
        sck.send(headerPack)
        sck.send(resCode + resReason)
        # print "resCode:",resCode
        # print "resReason:",resReason
        # print "params:",params