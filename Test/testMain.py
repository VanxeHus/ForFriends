#!usr/bin/python
#coding=utf-8
import socket
import struct
import time
import utils.config.SocketConfig as sCon
if __name__=='__main__':
    s=socket.socket(sCon.IPV4,sCon.TCP)
    s.connect((sCon.HOST, sCon.PORT1))
#三个测试用例
#a:正常
    a='VanxeHus\t\n'
    header=a.__len__()
    headerPack=struct.pack('>I4s',header,"USER")
    s.send(headerPack)
    s.send(a)
    #print("header a:%s"%header)
#b:包不足
    b='TESTING\t\n'
    b1='cwdtest'
    header=b.__len__()+b1.__len__()
    headerPack=struct.pack(">I4s",header,"CWPD")
    s.send(headerPack)
    time.sleep(3)
    s.send(b+b1)
    #print("header a:%s" % header)
#c:多包
    c='TESTING\t\n'
    header=c.__len__()
    headerPack=struct.pack(">I4s",header,"FILE")
    for i in range(0,10):
        s.send(headerPack)
        s.send(c)



