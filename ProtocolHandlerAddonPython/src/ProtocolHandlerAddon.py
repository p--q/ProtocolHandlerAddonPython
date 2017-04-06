#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import uno
import unohelper
from com.sun.star.lang import XServiceInfo
from com.sun.star.lang import XInitialization
from com.sun.star.frame import XDispatchProvider
from com.sun.star.frame import XDispatch
IMPLE_NAME = "ProtocolHandlerAddonImpl"
SERVICE_NAME = "com.sun.star.frame.ProtocolHandler"
class ProtocolHandlerAddon(unohelper.Base,XServiceInfo,XDispatchProvider,XDispatch,XInitialization):
    def __init__(self,ctx, *args):
        self.ctx = ctx
        self.args = args
        self.smgr = ctx.ServiceManager
        self.frame = None
  
  
  
    # XInitialization
    def initialize(self,objects):
        if len(objects) > 0:
            self.frame = objects[0]
        
    
    
    # XServiceInfo
    def getImplementationName(self):
        return IMPLE_NAME
    def supportsService(self, name):
        return name == SERVICE_NAME
    def getSupportedServiceNames(self):
        return (SERVICE_NAME,)       
g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(ProtocolHandlerAddon,"ProtocolHandlerAddonImpl",("com.sun.star.frame.ProtocolHandler",),)
