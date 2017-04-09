#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import uno
import unohelper
from com.sun.star.lang import XServiceInfo
from com.sun.star.lang import XInitialization
from com.sun.star.frame import XDispatchProvider
from com.sun.star.frame import XDispatch
IMPLE_NAME = "ProtocolHandlerAddonImpl"  # 実装サービス名
SERVICE_NAME = "com.sun.star.frame.ProtocolHandler"  # サービス名
HANDLED_PROTOCOL = "org.openoffice.Office.addon.example:"  # プロトコール名
class ProtocolHandlerAddon(unohelper.Base,XServiceInfo,XDispatchProvider,XDispatch,XInitialization):
    def __init__(self,ctx, *args):
        self.ctx = ctx
        self.args = args
        self.smgr = ctx.ServiceManager
        self.frame = None
    # XInitializationの実装
    def initialize(self,objects):
        if len(objects) > 0:
            self.frame = objects[0]
    # XServiceInfoの実装
    def getImplementationName(self):
        return IMPLE_NAME
    def supportsService(self, name):
        return name == SERVICE_NAME
    def getSupportedServiceNames(self):
        return (SERVICE_NAME,)       
    # XDispatchProviderの実装 コマンドURLを受け取ってXDispatchを備えたオブジェクトを返す。今回は自身を返している。
    def queryDispatch(self,aURL,name,flag): 
        dispatch = None
        if aURL.Protocol == HANDLED_PROTOCOL:
            if aURL.Path in ["Function1","Function2","Help"]:
                dispatch = self
        return dispatch
    def queryDispatches(self,descs):
        dispatchers = []
        for desc in descs:
            dispatchers.append(
                self.queryDispatch(desc.FeatureURL,desc.FrameName,desc.SearchFlags))
        return tuple(dispatchers)    
    # XDispatchの実装　コマンドURLを受け取って処理する。
    def dispatch(self,aURL,args):
        if aURL.Protocol == HANDLED_PROTOCOL:
            if aURL.Path == "Function1":
                self.showMessageBox("SDK DevGuide Add-On example", "Function 1 activated by Python UNO Component")
            elif aURL.Path == "Function2":
                self.showMessageBox("SDK DevGuide Add-On example", "Function 2 activated by Python UNO Component") 
            elif aURL.Path == "Help":
                self.showMessageBox("About SDK DevGuide Add-On example", "This is the SDK Add-On example by Python UNO Component") 
    def addStatusListener(self,xControl,aURL):
        pass
    def removeStatusListener(self,xControl,aURL):
        pass
    # このクラスのメソッド。
    def showMessageBox(self,title, msg):
        win = self.frame.getContainerWindow()
        toolkit = win.getToolkit()
        msgbox = toolkit.createMessageBox(win, "INFOBOX", 1, title, msg)
        msgbox.execute()
g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(ProtocolHandlerAddon,IMPLE_NAME,(SERVICE_NAME,),)
