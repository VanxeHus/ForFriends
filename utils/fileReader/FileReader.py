#!usr/bin/python
#coding=utf-8
import os

from utils.config import FileConfig
from utils.log import logEvent

@logEvent.LogExcept
def InitFile_list():
    filePath=FileConfig.FilePos
    if os.access(filePath,os.F_OK) and os.access(filePath,os.R_OK):
        res=os.listdir()
        resStr=""
        for value in res:
            resStr+=value+"\t\n"
    return resStr
@logEvent.LogExcept
def PlayFile():
    pass
def ReadFile(pos):
    filePath=FileConfig.FilePos+"/"+pos

    #读取子文件或者播放
    resStr=""
    if os.path.isdir(filePath):
        if os.access(filePath, os.F_OK) and os.access(filePath, os.R_OK):
            res=os.listdir(filePath)
            for value in res:
                resStr+=value+"\t\n"
    elif os.path.isfile(filePath):
        resStr="play Success"
    return resStr

