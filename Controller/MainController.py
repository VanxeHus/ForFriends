#!usr/bin/python
# coding=utf-8
from Implement import LoginController as Login
from Implement import NotfindController as Notfind
from Implement import FileController as File


class MainController:
    def __init__(self):
        self.cMap = {}

    # 分发数据包到各个子controller
    # data包括header和body
    def Handle(self, sck, addr, data):
        if not (data.has_key("Header") or data.has_key("Body")):
            raise NameError, "data.Header or data.Body is null"
        if self.cMap.has_key(data["Header"][1]):
            self.cMap[data["Header"][1]]().Handle(sck, addr, data)
        else:
            self.cMap["404"]().Handle(sck, addr, data)

    # 注册子controller
    def RigistController(self, key, type):
        if key and type:
            self.cMap[key] = type
        else:
            raise NameError, "key or type is null"
#注册子controller
def regist():
    mainController.RigistController("USER", Login.LoginController)
    mainController.RigistController("FILE", File.FileController)
    mainController.RigistController("404", Notfind.NotfindController)
# 获取全局唯一的mainController
def GetInstance():
    global mainController
    if mainController:
        return mainController
    else:
        mainController = MainController()
        return mainController

mainController = MainController()
regist()

