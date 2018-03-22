#!usr/bin/python
# coding=utf-8
import socket
import struct
import threading
import utils.log.logEvent as log
import utils.config.SocketConfig as sCon
from Controller import MainController

@log.LogExcept
@log.LogEvent('DEBUG')
def handle(sck, addr):
    dataBuf = ''
    while True:
        dataBuf += sck.recv(1024)
        # 若达到包头长度则处理
        if len(dataBuf) >= sCon.HEADER_SIZE:
            # 读包头
            header = struct.unpack('>I4s', dataBuf[:sCon.HEADER_SIZE])
            # 若达到body长度则处理
            if len(dataBuf) >= sCon.HEADER_SIZE + header[0]:
                body = dataBuf[sCon.HEADER_SIZE:sCon.HEADER_SIZE + header[0]]
                # 数据包字典
                data = {"header": header, "body": body}
                MainController.GetInstance().Handle(sck, addr, data)
                # 抛弃已经处理完的数据包
                dataBuf = dataBuf[sCon.HEADER_SIZE + header[0]:]
            else:
                raise NameError, "body's len is:%s not enough" % (len(dataBuf) - sCon.HEADER_SIZE)
        else:
            raise NameError, "data'len is:%s not enough" % len(dataBuf)


def Main():
    s = socket.socket(sCon.IPV4, sCon.TCP)
    s.bind((sCon.HOST, sCon.PORT1))
    s.listen(5)

    sckDist = {}
    while True:
        print("----fucking listening----")
        newSck, addr = s.accept()
        threading._start_new_thread(handle, (newSck, addr))
        sckDist[addr] = newSck


if __name__ == '__main__':
    Main()
