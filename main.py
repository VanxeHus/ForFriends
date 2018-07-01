#!usr/bin/python
# coding=utf-8
import socket
import struct
import threading
import time

import utils.log.logEvent as log
import utils.config.SocketConfig as sCon
import utils.config.SessionConfig as sessCon
from Model import SessionManager
from Controller import MainController

@log.LogExcept
@log.LogEvent('Main')
def handle(sck, addr):
    dataBuf = ""
    startTime=time.time()
    while True:
        dataBuf += sck.recv(1024)
        nowTime=time.time()
        # 若达到包头长度则处理
        if len(dataBuf) >= sCon.HEADER_SIZE:
            # 读包头
            startTime=time.time()
            header = struct.unpack('>I4s', dataBuf[:sCon.HEADER_SIZE])
            #print header
            # 若达到body长度则处理
            if len(dataBuf) >= sCon.HEADER_SIZE + header[0]:
                body = dataBuf[sCon.HEADER_SIZE:sCon.HEADER_SIZE + header[0]]
                # 分割body
                # 获取body中各参数
                bDic = body.split()
                print "bDic:",bDic
                bMap = {}
                for value in bDic:
                    tDic = value.split(":")
                    if len(tDic) > 1:
                        bMap[tDic[0]] = tDic[1]
                print "bMap:",bMap
                # 数据包字典
                data = {"Header": header, "Body": bMap}
                MainController.GetInstance().Handle(sck, addr, data)
                # 抛弃已经处理完的数据包
                dataBuf = dataBuf[sCon.HEADER_SIZE + header[0]:]
            else:
                #raise NameError, "body's len is:%s not enough" % (len(dataBuf) - sCon.HEADER_SIZE)
                continue
        else:
            if nowTime-startTime >sCon.ALIVE:
                sck.close()
                removeSocket(addr)
                return
            else:
            #raise NameError, "data'len is:%s not enough" % len(dataBuf)
                continue

@log.LogExcept
@log.LogEvent('delete socket')
def removeSocket(addr):
    global sckDist
    sckDist.pop(addr)

sckDist = {}

def Main():
    s = socket.socket(sCon.IPV4, sCon.TCP)
    s.bind((sCon.HOST, sCon.PORT2))
    s.listen(5)
    # sessionManager
    # Destroy session in time
    threading._start_new_thread(SessionManager.GetInstance().TD,())

    # socketManage
    while True:
        #print("----fucking listening----")
        newSck, addr = s.accept()
        threading._start_new_thread(handle, (newSck, addr))
        global sckDist
        sckDist[addr] = newSck


if __name__ == '__main__':
    Main()
