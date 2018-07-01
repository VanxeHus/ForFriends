#!usr/bin/python
#coding=utf-8
import os

from utils.config import FileConfig
from utils.log import logEvent

@logEvent.LogExcept
def InitFile_list():
    filePath=FileConfig.FilePos
    resStr = "file:"
    if os.access(filePath,os.F_OK) and os.access(filePath,os.R_OK):
        res=os.listdir(filePath)
        resStr+=str(len(res))+"\t\n"
        fileNum=1
        for value in res:
            resStr+="file%d:"%(fileNum)+value+"\t\n"
            fileNum+=1
    if len(resStr)<=0:
        resStr="\t\n"
    return resStr
@logEvent.LogExcept
def PlayFile(filePath):
    pass
def ReadFile(pos):
    filePath=FileConfig.FilePos+"/"+pos

    #读取子文件或者播放
    resStr="file:"
    if os.path.isdir(filePath):
        if os.access(filePath, os.F_OK) and os.access(filePath, os.R_OK):
            res=os.listdir(filePath)
            resStr += str(len(res)) + "\t\n"
            fileNum = 1
            for value in res:
                resStr += "file%d:" % (fileNum) + value + "\t\n"
                fileNum += 1
    elif os.path.isfile(filePath):
        PlayFile(filePath)
        resStr+="play success"
    return resStr

