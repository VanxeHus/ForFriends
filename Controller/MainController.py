#!usr/bin/python
#coding=utf-8
from Implement import LoginController as Login
from Implement import NotfindController as Notfind
class MainController:
    def __init__(self):
        self.cMap={}
    #分发数据包到各个子controller
    #data包括header和body
    def Handle(self,sck,addr,data):
        if len(data.header)<=0 or len(data.body)<=0:
            raise NameError,"data.header or data.body is null"
        if self.cMap.has_key(data.header[1]):
            self.cMap[data.header[1]]().Handle(sck,addr,data)
        else:
            self.cMap["400"]().Handle(sck,addr,data)
    #注册子controller
    def RigistController(self,key,type):
        if key and type:
            self.cMap[key]=type
        else:
            raise NameError,"key or type is null"

mainController=MainController()
mainController.RigistController("USER",Login.LoginController)
mainController.RigistController("404",Notfind.NotfindController)
#获取全局唯一的mainController
def GetInstance():
    global mainController
    if mainController:
        return mainController
    else:
        mainController=MainController()
        return mainController

