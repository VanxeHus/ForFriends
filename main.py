#!usr/bin/python
# coding=utf-8
import socket
import struct
import threading
import utils.log.logEvent as log
import utils.config.SocketConfig as sCon


@log.LogEvent('DEBUG')
def handle(newSocket, addr):
    dataBuf=''
    while True:
        dataBuf += newSocket.recv(1024)
        #若达到包头长度则处理
        if len(dataBuf) >= sCon.HEADER_SIZE:
            #读包头
            header = struct.unpack('>I', dataBuf[:sCon.HEADER_SIZE])
            #若达到body长度则处理
            if len(dataBuf) >= sCon.HEADER_SIZE + header[0]:
                body = dataBuf[sCon.HEADER_SIZE:sCon.HEADER_SIZE + header[0]]
                # passHandle
                dataBuf = dataBuf[sCon.HEADER_SIZE + header[0]:]
            else:
                print("body's len is:%s not enough"%(len(dataBuf) - sCon.HEADER_SIZE))
                pass
        else:
            print("data'len is:%s not enough"%len(dataBuf))
            pass


def Main():
    s = socket.socket(sCon.IPV4, sCon.TCP)
    s.bind((sCon.HOST, sCon.PORT1))
    s.listen(5)

    sckDist = {}
    while True:
        print("----fucking listening----")
        newSck, addr = s.accept()
        threading._start_new_thread(handle, (newSck,addr))
        sckDist[addr] = newSck


if __name__ == '__main__':
    Main()
