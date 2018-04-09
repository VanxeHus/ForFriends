#!usr/bin/python
#coding=utf-8
import struct

from Model import MysqlManager
from Model import SessionManager
from utils.log import logEvent
from utils.encrypt import MD5
from utils.fileReader import FileReader


class FileController:
    def __init__(self):
        pass
    @logEvent.LogEvent("FileHandle")
    def Handle(self,sck,addr,data):
        body=data["Body"]
        #获取session
        sess=SessionManager.GetInstance().SessionStart(None,body["Sid"])

        #结果
        resCode=""
        resReason=""
        params=""
        #无效身份
        if sess is None:
            resCode="401\t\n"
            resReason="Unauthorized\t\n"
        else:
            ret=FileReader.ReadFile(body["File"])
            if ret[:4]=="play ":
                if ret[5:]=="success":
                    resCode="200\t\n"
                else:
                    resCode="500\t\n"
                resReason="%s\t\n"%ret
            else:
                resCode="200\t\n"
                resReason="ReadFile success\t\n"
                params="files:%s"%ret

        #发送数据
        headerLen=resCode.__len__()+resReason.__len__()+params.__len__()
        headerPack=struct.pack(">I4s",headerLen,"FILE")
        sck.send(headerPack)
        sck.send(resCode + resReason + params)
        # print "resCode:",resCode
        # print "resReason:",resReason
        # print "params:",params