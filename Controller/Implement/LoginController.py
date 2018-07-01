#!usr/bin/python
# coding=utf-8

import struct

from utils.log import logEvent
from Model import MysqlManager
from utils.encrypt import MD5
from Model import SessionManager
from utils.fileReader import FileReader


class LoginController:
    def __init__(self):
        pass

    @logEvent.LogExcept
    @logEvent.LogEvent("LoginHandle")
    def Handle(self, sck, addr, data):
        resCode = ""
        resReason = ""
        params = ""
        body = data["Body"]
        # 处理
        if body is {}:
            resCode = "400\t\n"
            resReason = "paras is null\t\n"
        else:
            user = MysqlManager.GetInstance().getUser(body["User"])
            if not user:
                # 用户名不存在
                resCode = "401\t\n"
                resReason = "Unauthorized\t\n"
            elif MD5.MD5Encrypto_withSalt(body["Pwd"], user["Salt"]) != user["Pwd"]:
                # 密码错误
                resCode = "402\t\n"
                resReason = "Pwd wrong\t\n"
            else:
                # 创建或返回session
                sess = SessionManager.GetInstance().SessionStart(body)
                if sess is not None:
                    resCode = "200\t\n"
                    resReason = "Login success\t\n"
                    # 读取视频文件列表
                    fileList = FileReader.InitFile_list()
                    params = "sid:%s\t\n%s" % (sess.SessionId(), fileList)
                else:
                    resCode = "500\t\n"
                    resReason = "Session create fail\t\n"
        # 发送处理结果
        headerLen = resCode.__len__() + resReason.__len__() + params.__len__()
        headerPack = struct.pack(">I4s", headerLen, "USER")
        sck.send(headerPack)
        sck.send(resCode + resReason + params)
        print "resCode:%sresReason:%sparams:%s" % (resCode, resReason, params)
        return
        #print "headerlen:%s" % headerLen
        # print "resCode:",resCode
        # print "resReason:",resReason
        # print "params:",params
