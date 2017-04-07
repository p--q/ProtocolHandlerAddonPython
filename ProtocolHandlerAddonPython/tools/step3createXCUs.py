#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import sys
from step1settings import LST
from step2createRDB import src_path
class Elem(ET.Element):  # textも引数で設定できるようにするクラス。
    def __init__(self, tag, attrib={}, text=None, **extra):  
        attrib.update(extra)       
        super().__init__(tag, attrib)
        if text:
            self._text(text)
    def _text(self,text):
        self.text = text
class MenuItem():
    def __init__(self,dic,mdic):
        self.dic = dic
        self.mdic = mdic
    def create(self):
        lst_nd = list()
        for key,val in self.mdic.items():
            if key == "Title":
                snd = Elem("prop",{"oor:name":key,"oor:type":"xs:string"})
                for lang,txt in val.items():
                    snd.append(Elem("value",{"xml:lang":lang}),text=txt)
                lst_nd.append(snd)
            elif key == "Submenu":
                lst_nd.append(self.subMenu(key, val))
            else:
                lst_nd.append(Elem("value",text=val))
        return lst_nd          
    def subMenu(self,key,val):
        '''
        
        :param key:
        :param val:
        '''
        
        pass
        
        
        
def createOfficeMenuBarSubMenu(dic,key,val):
    snd = Elem("node",{"oor:name":key,"oor:type":"xs:string"})
    ssnd = Elem("node",{"oor:name":val[0],"oor:op":"replace"})
    ssnd.append(createAddonMenu(dic,{"URL":dic[IMPLE_NAME] + ":Function1","ImageIdentifier":"","Title":"Add-On Function 1","Target":"_self","Context":"com.sun.star.text.TextDocument"}))
    snd.append(ssnd)
    ssnd = Elem("node",{"oor:name":val[1],"oor:op":"replace"})
    ssnd.append(createAddonMenu(dic,{"URL":"private:separator"}))
    snd.append(ssnd)
    ssnd = Elem("node",{"oor:name":val[2],"oor:op":"replace"})
    ssnd.append(createAddonMenu(dic,{"URL":"","ImageIdentifier":"","Title":"Add-On sub menu","Target":"_self","Submenu":["m1"]}))
    snd.append(ssnd)            
    return snd               
def createAddonSubMenu(dic,key,val):  
    snd = Elem("node",{"oor:name":key,"oor:type":"xs:string"})
    ssnd = Elem("node",{"oor:name":val[0],"oor:op":"replace"})
    ssnd.append(createAddonMenu(dic,{"URL":dic[IMPLE_NAME] + ":Function1","ImageIdentifier":"","Title":"Add-On Function 1","Target":"_self"}))
    snd.append(ssnd)
    ssnd = Elem("node",{"oor:name":val[1],"oor:op":"replace"})
    ssnd.append(createAddonMenu(dic,{"URL":dic[IMPLE_NAME] + ":Function2","ImageIdentifier":"","Title":"Add-On Function 2","Target":"_self"}))
    snd.append(ssnd)
    return snd   
def createMenuItem(dic,mdic,fnSubMenu):
    lst_nd = list()
    for key,val in mdic.items():
        if key == "Title":
            snd = Elem("prop",{"oor:name":key,"oor:type":"xs:string"})
            for lang,txt in val.items():
                snd.append(Elem("value",{"xml:lang":lang}),text=txt)
            lst_nd.append(snd)
        elif key == "Submenu":
            lst_nd.append(fnSubMenu(dic,key,val))
        else:
            lst_nd.append(Elem("value",text=val))
    return lst_nd  
def createAddonMenu(dic,mdic):
    nd = Elem("node",{'oor:name':"AddonMenu"})
    nd.append(Elem("node",{'oor:name':dic[IMPLE_NAME] + ".function","oor:op":"replace"}))
    nd[0].extend(createMenuItem(dic,mdic,createAddonSubMenu))
    return nd
def createImages(dic,mdic):
    pass
def createOfficeMenuBar(dic,mdic):
    nd = Elem("node",{'oor:name':dic[IMPLE_NAME],"oor:op":"replace"})
    nd.append(Elem("node",{'oor:name':dic[IMPLE_NAME],"oor:op":"replace"}))
    nd[0].extend(createMenuItem(dic,mdic,createOfficeMenuBarSubMenu))
    return nd    
def createOfficeToolBar(dic,mdic):
    pass
def createOfficeHelp(dic,mdic):
    pass
def main():
    #Creation of ProtocolHandler.xcu
    os.chdir(src_path)  # srcフォルダに移動。
    for dic in LST:  # 設定リストの各辞書について
        if "HANDLED_PROTOCOL" in dic:  # HANDLED_PROTOCOLが辞書のキーにあるとき       
            with open("ProtocolHandler.xcu","w",encoding="utf-8") as fp:
                rt = Elem("oor:component-data",{"oor:name":"ProtocolHandler","oor:package":"org.openoffice.Office","xmlns:oor":"http://openoffice.org/2001/registry","xmlns:xs":"http://www.w3.org/2001/XMLSchema","xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"})  # 根の要素を作成。
                rt.append(Elem("node",{'oor:name':"HandlerSet"}))
                rt[0].append(Elem("node",{'oor:name':dic[IMPLE_NAME],"oor:op":"replace"}))
                rt[0][0].append(Elem("prop",{'oor:name':"Protocols","oor:type":"oor:string-list"}))
                rt[0][0][0].append(Elem("value",text = dic[HANDLED_PROTOCOL] + ":*"))
                tree = ET.ElementTree(rt)  # 根要素からxml.etree.ElementTree.ElementTreeオブジェクトにする。
                tree.write(fp.name,"utf-8",True)  # xml_declarationを有効にしてutf-8でファイルに出力する。   
                print("ProtocolHandler.xcu has been created.")    
            #Creation of Addons.xcu
            addons = os.path.join(src,"Addons.xcu")    
            with open(addons,"w",encoding="utf-8") as fp:   
                rt = Elem("oor:component-data",{"oor:name":"Addons","oor:package":"org.openoffice.Office","xmlns:oor":"http://openoffice.org/2001/registry","xmlns:xs":"http://www.w3.org/2001/XMLSchema"})  # 根の要素を作成。
                rt.append(Elem("node",{'oor:name':"AddonUI"}))
                rt[0].extend([
                    createAddonMenu(dic,{"Title":{"en-US":"Add-On example"},"Context":"com.sun.star.text.TextDocument","Submenu":["m1","m2"]}),
                    createOfficeMenuBar(dic,{"Title":{"en-US":"Add-On example"},"Target":"_self","ImageIdentifier":"","Submenu":["m1","m2","m3"]})
                    
                    ])
                
                
                a = 0
                rt[a].append(Elem("node",{'oor:name':"AddonMenu"}))
                rt[a].append(Elem("node",{'oor:name':"OfficeMenuBar"}))
                rt[a].append(Elem("node",{'oor:name':"OfficeToolBar"}))
                rt[a].append(Elem("node",{'oor:name':"Images"}))
                rt[a].append(Elem("node",{'oor:name':"OfficeHelp"}))
                b = 0
                rt[a][b].append(Elem("node",{"oor:name":"org.openoffice.Office.addon.example.function","oor:op":"replace"}))
                c = 0
                rt[a][b][c].append(Elem("prop",{"oor:name":"Title","oor:type":"xs:string"}))
                rt[a][b][c].append(Elem("prop",{"oor:name":"Context","oor:type":"xs:string"}))
                rt[a][b][c].append(Elem("node",{"oor:name":"Submenu"}))     
                d = 0                                 
                rt[a][b][c][d].append(Elem("value",{"xml:lang":"en-US"},text="Add-On example"))
                d += 1
                rt[a][b][c][d].append(Elem("value",text="com.sun.star.text.TextDocument"))
                d += 1
                rt[a][b][c][d].append(Elem("node",{"oor:name":"m1","oor:op":"replace"})) 
                rt[a][b][c][d].append(Elem("node",{"oor:name":"m2","oor:op":"replace"})) 
                e = 0
                rt[a][b][c][d][e].append(Elem("prop",{"oor:name":"URL","oor:type":"xs:string"})) 
                rt[a][b][c][d][e].append(Elem("prop",{"oor:name":"ImageIdentifier","oor:type":"xs:string"}))
                rt[a][b][c][d][e].append(Elem("prop",{"oor:name":"Title","oor:type":"xs:string"}))
                rt[a][b][c][d][e].append(Elem("prop",{"oor:name":"Target","oor:type":"xs:string"}))
                f = 0
                rt[a][b][c][d][e][f].append(Elem("value",text="org.openoffice.Office.addon.example:Function1"))
                f += 1
                rt[a][b][c][d][e][f].append(Elem("value")) 
                f += 1
                rt[a][b][c][d][e][f].append(Elem("value")) 
                rt[a][b][c][d][e][f].append(Elem("value",{"xml:lang":"en-US"},text="Add-On Function 1"))
                f += 1
                rt[a][b][c][d][e][f].append(Elem("value",text="_self")) 
                e += 1
                rt[a][b][c][d][e].append(Elem("prop",{"oor:name":"URL","oor:type":"xs:string"})) 
                rt[a][b][c][d][e].append(Elem("prop",{"oor:name":"ImageIdentifier","oor:type":"xs:string"}))
                rt[a][b][c][d][e].append(Elem("prop",{"oor:name":"Title","oor:type":"xs:string"}))
                rt[a][b][c][d][e].append(Elem("prop",{"oor:name":"Target","oor:type":"xs:string"}))
                f = 0
                rt[a][b][c][d][e][f].append(Elem("value",text="org.openoffice.Office.addon.example:Function2"))
                f += 1
                rt[a][b][c][d][e][f].append(Elem("value")) 
                f += 1
                rt[a][b][c][d][e][f].append(Elem("value")) 
                rt[a][b][c][d][e][f].append(Elem("value",{"xml:lang":"en-US"},text="Add-On Function 2"))
                f += 1
                rt[a][b][c][d][e][f].append(Elem("value",text="_self")) 
                b += 1
                rt[a][b].append(Elem("node",{"oor:name":"org.openoffice.Office.addon.example","oor:op":"replace"}))
                c = 0
                rt[a][b][c].append(Elem("prop",{"oor:name":"Title","oor:type":"xs:string"}))
                rt[a][b][c].append(Elem("prop",{"oor:name":"Target","oor:type":"xs:string"}))
                rt[a][b][c].append(Elem("prop",{"oor:name":"ImageIdentifier","oor:type":"xs:string"}))
                rt[a][b][c].append(Elem("node",{"oor:name":"Submenu"}))     
                d = 0 
                rt[a][b][c][d].append(Elem("value"))                                
                rt[a][b][c][d].append(Elem("value",{"xml:lang":"en-US"},text="Add-On example"))
                d += 1
                rt[a][b][c][d].append(Elem("value",text="_self"))
                d += 1
                rt[a][b][c][d].append(Elem("value")) 
                d += 1
                rt[a][b][c][d].append(Elem("node",{"oor:name":"m1","oor:op":"replace"}))
                rt[a][b][c][d].append(Elem("node",{"oor:name":"m2","oor:op":"replace"})) 
                rt[a][b][c][d].append(Elem("node",{"oor:name":"m3","oor:op":"replace"})) 
                e = 0
                rt[a][b][c][d][e].append(Elem("prop",{"oor:name":"URL","oor:type":"xs:string"})) 
                rt[a][b][c][d][e].append(Elem("prop",{"oor:name":"ImageIdentifier","oor:type":"xs:string"}))
                rt[a][b][c][d][e].append(Elem("prop",{"oor:name":"Title","oor:type":"xs:string"}))
                rt[a][b][c][d][e].append(Elem("prop",{"oor:name":"Target","oor:type":"xs:string"}))
                rt[a][b][c][d][e].append(Elem("prop",{"oor:name":"Context","oor:type":"xs:string"}))
                f = 0
                rt[a][b][c][d][e][f].append(Elem("value",text="org.openoffice.Office.addon.example:Function1"))
                f += 1
                rt[a][b][c][d][e][f].append(Elem("value")) 
                f += 1
                rt[a][b][c][d][e][f].append(Elem("value")) 
                rt[a][b][c][d][e][f].append(Elem("value",{"xml:lang":"en-US"},text="Add-On Function 1"))
                f += 1
                rt[a][b][c][d][e][f].append(Elem("value",text="_self")) 
                f += 1
                rt[a][b][c][d][e][f].append(Elem("value",text="com.sun.star.text.TextDocument")) 
                e += 1
                rt[a][b][c][d][e].append(Elem("prop",{"oor:name":"URL","oor:type":"xs:string"})) 
                f = 0
                rt[a][b][c][d][e][f].append(Elem("value",text="private:separator"))
                e += 1
                rt[a][b][c][d][e].append(Elem("prop",{"oor:name":"URL","oor:type":"xs:string"})) 
                rt[a][b][c][d][e].append(Elem("prop",{"oor:name":"ImageIdentifier","oor:type":"xs:string"}))
                rt[a][b][c][d][e].append(Elem("prop",{"oor:name":"Title","oor:type":"xs:string"}))
                rt[a][b][c][d][e].append(Elem("prop",{"oor:name":"Target","oor:type":"xs:string"}))
                rt[a][b][c][d][e].append(Elem("node",{"oor:name":"Submenu"}))
                f = 0
                rt[a][b][c][d][e][f].append(Elem("value"))
                f += 1
                rt[a][b][c][d][e][f].append(Elem("value")) 
                f += 1
                rt[a][b][c][d][e][f].append(Elem("value")) 
                rt[a][b][c][d][e][f].append(Elem("value",{"xml:lang":"en-US"},text="Add-On sub menu"))
                f += 1
                rt[a][b][c][d][e][f].append(Elem("value",text="_self")) 
                f += 1
                rt[a][b][c][d][e][f].append(Elem("node",{"oor:name":"submenu1","oor:op":"replace"})) 
                g = 0
                rt[a][b][c][d][e][f][g].append(Elem("prop",{"oor:name":"URL","oor:type":"xs:string"})) 
                rt[a][b][c][d][e][f][g].append(Elem("prop",{"oor:name":"ImageIdentifier","oor:type":"xs:string"}))
                rt[a][b][c][d][e][f][g].append(Elem("prop",{"oor:name":"Title","oor:type":"xs:string"}))
                rt[a][b][c][d][e][f][g].append(Elem("prop",{"oor:name":"Target","oor:type":"xs:string"}))
                rt[a][b][c][d][e][f][g].append(Elem("prop",{"oor:name":"Context","oor:type":"xs:string"}))
                h = 0
                rt[a][b][c][d][e][f][g][h].append(Elem("value",text="org.openoffice.Office.addon.example:Function2"))
                h += 1
                rt[a][b][c][d][e][f][g][h].append(Elem("value")) 
                h += 1
                rt[a][b][c][d][e][f][g][h].append(Elem("value")) 
                rt[a][b][c][d][e][f][g][h].append(Elem("value",{"xml:lang":"en-US"},text="Add-On Function 2"))
                h += 1
                rt[a][b][c][d][e][f][g][h].append(Elem("value",text="_self")) 
                h += 1
                rt[a][b][c][d][e][f][g][h].append(Elem("value",text="com.sun.star.sheet.SpreadsheetDocument")) 
                b += 1
                rt[a][b].append(Elem("node",{"oor:name":"org.openoffice.Office.addon.example","oor:op":"replace"}))
                c = 0
                rt[a][b][c].append(Elem("node",{"oor:name":"m1","oor:op":"replace"})) 
                rt[a][b][c].append(Elem("node",{"oor:name":"m2","oor:op":"replace"})) 
                d = 0
                rt[a][b][c][d].append(Elem("prop",{"oor:name":"URL","oor:type":"xs:string"})) 
                rt[a][b][c][d].append(Elem("prop",{"oor:name":"ImageIdentifier","oor:type":"xs:string"}))
                rt[a][b][c][d].append(Elem("prop",{"oor:name":"Title","oor:type":"xs:string"}))
                rt[a][b][c][d].append(Elem("prop",{"oor:name":"Target","oor:type":"xs:string"}))
                rt[a][b][c][d].append(Elem("prop",{"oor:name":"Context","oor:type":"xs:string"}))
                e = 0
                rt[a][b][c][d][e].append(Elem("value",text="org.openoffice.Office.addon.example:Function1"))
                e += 1
                rt[a][b][c][d][e].append(Elem("value")) 
                e += 1
                rt[a][b][c][d][e].append(Elem("value")) 
                rt[a][b][c][d][e].append(Elem("value",{"xml:lang":"en-US"},text="Function 1"))
                e += 1
                rt[a][b][c][d][e].append(Elem("value",text="_self")) 
                e += 1
                rt[a][b][c][d][e].append(Elem("value",text="com.sun.star.text.TextDocument")) 
                d += 1
                rt[a][b][c][d].append(Elem("prop",{"oor:name":"URL","oor:type":"xs:string"})) 
                rt[a][b][c][d].append(Elem("prop",{"oor:name":"ImageIdentifier","oor:type":"xs:string"}))
                rt[a][b][c][d].append(Elem("prop",{"oor:name":"Title","oor:type":"xs:string"}))
                rt[a][b][c][d].append(Elem("prop",{"oor:name":"Target","oor:type":"xs:string"}))
                rt[a][b][c][d].append(Elem("prop",{"oor:name":"Context","oor:type":"xs:string"}))
                e = 0
                rt[a][b][c][d][e].append(Elem("value",text="org.openoffice.Office.addon.example:Function2"))
                e += 1
                rt[a][b][c][d][e].append(Elem("value")) 
                e += 1
                rt[a][b][c][d][e].append(Elem("value")) 
                rt[a][b][c][d][e].append(Elem("value",{"xml:lang":"en-US"},text="Function 2"))
                e += 1
                rt[a][b][c][d][e].append(Elem("value",text="_self")) 
                e += 1
                rt[a][b][c][d][e].append(Elem("value",text="com.sun.star.text.TextDocument"))         
                b += 1
                rt[a][b].append(Elem("node",{"oor:name":"com.sun.star.comp.framework.addon.image1","oor:op":"replace"}))
                rt[a][b].append(Elem("node",{"oor:name":"com.sun.star.comp.framework.addon.image2","oor:op":"replace"})) 
                c = 0
                rt[a][b][c].append(Elem("prop",{"oor:name":"URL"}))
                rt[a][b][c].append(Elem("node",{"oor:name":"UserDefinedImages"}))
                d = 0
                rt[a][b][c][d].append(Elem("value",text="org.openoffice.Office.addon.example:Function1"))
                d += 1
                rt[a][b][c][d].append(Elem("prop",{"oor:name":"ImageSmall","oor:type":"xs:hexBinary"}))
                rt[a][b][c][d].append(Elem("prop",{"oor:name":"ImageBig","oor:type":"xs:hexBinary"}))
                rt[a][b][c][d].append(Elem("prop",{"oor:name":"ImageSmallHC","oor:type":"xs:hexBinary"}))
                rt[a][b][c][d].append(Elem("prop",{"oor:name":"ImageBigHC","oor:type":"xs:hexBinary"}))
                e = 0
                rt[a][b][c][d][e].append(Elem("value",text="424df80000000000000076000000280000001000000010000000010004000000000000000000120b0000120b000000000000000000000000ff0000ffff0000ff0000ffff0000ff000000ff00ff00ffffff00c0c0c0008080800000000000000080000080800000800000808000008000000080008000cccccccccccccccc2c266b181b666c2c5cc66b818b6665c555566b181b66655555566b818b66655555566b181b6665555a8666bbb6668a55a0a866666668a0a5000a8666668a000a6000a86668a000a556000a868a000a55556000a8a000a5555556000a000a55555555600000a55555555556000a55555555555560a55555550000"))
                e += 1
                rt[a][b][c][d][e].append(Elem("value",text="424d180200000000000076000000280000001a0000001a000000010004000000000000000000120b0000120b000000000000000000000000ff0000ffff0000ff0000ffff0000ff000000ff00ff00ffffff00c0c0c000808080000000000000008000008080000080000080800000800000008000800055555555555555555555555555999990cccccccccccccccccccccccccc9055552cc2c6666b18181b6666c2cc2c99ccccc2ccc6666b81818b66668c2cc5902cc25c2586666b18181b66668ccc5590c2cc555586666b81818b6666855555995c25555586666b18181b6666855555995555555586666b81818b6666855555005555555586666b18181b666685555590555555a5866666b181b6666685a5550955555a0a8666666bbb6666668a0a559955a5a000a866666666666668a000a5995a0a00000a8666666666668a00000a90a000600000a86666666668a00000a50900005600000a866666668a00000a5599600055600000a8666668a00000a555095600555600000a86668a00000a55559955605555600000a868a00000a5555599555655555600000a8a00000a555555005555555555600000a00000a555555590555555555556000000000a555555550955555555555560000000a555555555995555555555555600000a555555555590555555555555556000a555555555550055555555555555560a555555555555905555555555555555555555555555559055550000"))
                e += 1
                rt[a][b][c][d][e].append(Elem("value",text="424df60000000000000076000000280000001000000010000000010004000000000080000000120b0000120b000000000000000000000000ff0000ffff0000ff0000ffff0000ff000000ff00ff00ffffff00c0c0c00080808000000000000000800000808000008000008080000080000000800080002222222222222222222996969699922252299669669995255559969696999555555996696699955555599696969995555969996669996955969699999996969566696999996966699666969996966695596669696966695555966696966695555559666966695555555596666695555555555966695555555555559695555555"))
                e += 1
                rt[a][b][c][d][e].append(Elem("value"))
                c +=1
                rt[a][b][c].append(Elem("prop",{"oor:name":"URL"}))
                rt[a][b][c].append(Elem("node",{"oor:name":"UserDefinedImages"}))
                d = 0
                rt[a][b][c][d].append(Elem("value",text="org.openoffice.Office.addon.example:Help"))
                d += 1
                rt[a][b][c][d].append(Elem("prop",{"oor:name":"ImageSmall","oor:type":"xs:hexBinary"}))
                rt[a][b][c][d].append(Elem("prop",{"oor:name":"ImageBig","oor:type":"xs:hexBinary"}))
                rt[a][b][c][d].append(Elem("prop",{"oor:name":"ImageSmallHC","oor:type":"xs:hexBinary"}))
                rt[a][b][c][d].append(Elem("prop",{"oor:name":"ImageBigHC","oor:type":"xs:hexBinary"}))
                e = 0
                rt[a][b][c][d][e].append(Elem("value",text="424d36030000000000003600000028000000100000001000000001001800000000000003000000000000000000000000000000000000ff00ffff00ffff00ffff00fff0eeee6c5f602512133c2b2c2b1719594a4bdcd8d8ff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ff5443453a2525d0c5bdffffffffffffffffffe6e7e8493c3c5e514eb7b1b0ff00ffff00ffff00ffff00ffff00ff5c4a4dc0bbbcfffffffbeadee7bca8e7bcabdfb4a2f1c4b0fffffad0d0cd584a4dc5bbb8ff00ffff00ffff00ffddd9d9514449ffffffd49578b7511eb5582ed29d85ce8b6db54513ba5f32eeccb8fffffffffffbd3cfcfff00ffff00ffd9cdc5e0d9dadc9270ba4613bf511dc99076edeae7f2dcced27b54bc4811ba5724d3ad96ffffff402d30ff00ffefeae6e9e0daeabba4ba4308cb5b28cb5f2ecc7046d99979db8f66ce6635cc5d2dbf4e1ab85225ffeee5726361b1aaaad8cbc2ffffffbf4911c65b21cf6532cc5d2bcc764edbae97dfa284ce6a3bcc5b2bcc602ebb4310d28259ffffff332124d7cbc2fffffebb2600d0703bcc612ecb5b2bca7a56dfd3cdf5f4f1e1a686cd6333ce622dc95e2abe3901ffffff2b1a1dd8cdc4ffffffbe2f00d36f40cb602dcb5928c95a29ce8666e9ded7f1dcd2d77e56cd612acc6530c43a00ffffff312125d5c8beffffffcf3f00d66e3dcc632fc95d2ccb5522c44f19cf8c6becd4ccde9b81d06435d05b26c65619ffffff251317d9cdc5fefffff09361e87437da794ad29a7edfa68ad56f3bd5835bedd5cbe3b399d36939db6126e9b395ffffff3f3033f5f2f0ded6d1fff1e4f9a36ff28b52e3b39beeefedf3e5d9f2e7def4f0eaeba87ee66d2fee9e72fffffcb28d89c7c6c6ff00ffcbb6aaffffffffebdcfec08ff6b584edcebbeddaddf3dfdff5cab3f79c66fbaa7dfce8dcffffffb99e9bff00ffff00ffdccbc3e0d6cef2f2f2fffffcfff2d1fadca3f6cf91fac588fdc68bffe4c5fffefaffffffe2d4c8f2efeeff00ffff00ffff00fff0ebe6dfd0c9dbcac2f8f7f4fffffffffffffffffffdf8f2e3d9d1cfbfb4ebe3ddff00ffff00ffff00ffff00ffff00ffff00ffff00fffafaf9e1d6ced5c2b9d9c9c2d5c6beddcfc8f4f0efff00ffff00ffff00ffff00ffff00ff"))
                e += 1
                rt[a][b][c][d][e].append(Elem("value",text="424d560800000000000036000000280000001a0000001a00000001001800000000002008000000000000000000000000000000000000ff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ff0000ff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ff524142524142524142524142524142524142524142524142ff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ff0000ff00ffff00ffff00ffff00ffff00ffff00ff524142524142bda69cd6c7bddecfc6ded7d6e7dfd6e7d7cebdbebdb59694524142524142ff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ff0000ff00ffff00ffff00ffff00ffff00ff524142fffffffffffffffffffffffffffffffffffffffffff7f7f7ffffffffffffffefefbdb6ad524142524142ff00ffff00ffff00ffff00ffff00ffff00ff0000ff00ffff00ffff00ffff00ff524142ffffffffffffffffffefefefdedfdebdb6adc6a694d6a68cdebeade7d7ceefefeff7f7f7ffffffefe7deefe7de524142ff00ffff00ffff00ffff00ffff00ff0000ff00ffff00ffff00ffbda69cffffffffffffffffffefe7ded6a68cbd6139bd5929ce6942c6795abd5929bd5931ce8663debeadefefeffffffffff7f7efe7de524142ff00ffff00ffff00ffff00ff0000ff00ffff00ffff00ffbda69cffffffffffffe7cfc6ce7142bd5929bd5929bd6139d6c7bdffffffd69e84bd5929bd5929bd5929d69e7befefefffffffffefef524142ff00ffff00ffff00ffff00ff0000ff00ffff00ffdecfc6ffffffffffffe7cfc6c66139bd5929c66131ce6131bd7152dedfdeffffffe7c7bdce6131ce6131bd5929bd5929ce8e6befefefffffffdecfc6524142ff00ffff00ffff00ff0000ff00ffff00ffdecfc6ffffffefe7e7ce7142c66131ce6131ce6131ce6131c66131d6a68cefcfbdd68652ce6131ce6131ce6131c66131bd5929d6a68cffffffffffff524142ff00ffff00ffff00ff0000ff00ffdecfc6fff7f7ffffffdeae94bd5929ce6131ce6931ce6131ce6131ce6131ce6939d67142ce6131ce6131ce6131ce6131ce6131bd5929c66139f7dfd6ffffffdecfc6524142ff00ffff00ff0000ff00ffdecfc6fffffff7efefd6714ac66131ce6931ce6931ce6131ce6131c66939debeadffefe7de966bc66131ce6131ce6131ce6131ce6131bd5929deae94ffffffffefe7524142ff00ffff00ff0000ff00ffdecfc6ffffffefd7cece6131ce6931ce6931ce6131ce6131ce6131c66939d6d7d6ffffffdeb69cce6131ce6131ce6131ce6131ce6131bd5929ce8e63f7f7f7ffffff524142ff00ffff00ff0000ff00ffdecfc6ffffffefc7adce6131ce6939ce6931ce6131ce6131ce6131ce6131c6a694f7f7f7fff7efd68e63ce6131ce6131ce6131ce6931ce6131d6714af7efefffffff524142ff00ffff00ff0000ff00ffdecfc6ffffffefc7adce6131d66939ce6931ce6131ce6131ce6131ce6131c66139debeadfffffffff7efd68e63ce6131ce6931ce6931ce6131d6714af7efefffffff524142ff00ffff00ff0000ff00ffdecfc6ffffffffcfb5d67139d67142d66939ce6131ce6131ce6131ce6131ce6131c66939d6c7bdffffffffefefd6714ace6131d66939ce6931d68652fff7f7ffffff524142ff00ffff00ff0000ff00ffdecfc6ffffffffe7dee7794ade7142d67139ce6931ce6131ce6131ce6131ce6131ce6131ce7142f7efefffffffe7ae94ce6131d66939d66939d69673ffffffffffff524142ff00ffff00ff0000ff00ffdecfc6ffffffffffffefa67bef8652de7142d6714adebeadefdfcede9e7bce6131ce6131ce6131f7dfd6ffffffefc7add66939de7142d66939efc7b5ffffffffefef524142ff00ffff00ff0000ff00ffdecfc6f7f7f7ffffffffdfc6f7965af78e5ade794acecfceffffffffefe7d68652ce6131d69e84ffffffffffffdeae94d67139de7142ef9663fff7f7ffffffd6c7bd524142ff00ffff00ff0000ff00ffff00ffdecfc6fffffffffffff7c7adff9e6bf7965ad69e84efefeffffffffffff7ffefdeffffffffffffefe7e7ef9663e7864aef8652f7dfceffffffffffffb59694ff00ffff00ffff00ff0000ff00ffff00ffdecfc6f7f7efffffffffffffffd7adffb684ffa673efb69cdedfdeefefefefefefefefefefe7deefae8cf7965aff9663ffcfb5ffffffffffffdecfc6b59694ff00ffff00ffff00ff0000ff00ffff00ffff00ffdecfc6ffffffffffffffffffffefd6ffdfadffc794ffc794efb69cefb69cffbe9cffb684ffae7bffb68cffe7d6fffffffffffff7efe7bdb6adff00ffff00ffff00ffff00ff0000ff00ffff00ffff00ffff00ffdecfc6fffffffffffffffffffffff7ffffe7ffffd6ffefb5ffefb5ffdfadffdfadffefd6fffff7fffffffffffffff7efdecfc6ff00ffff00ffff00ffff00ffff00ff0000ff00ffff00ffff00ffff00ffff00ffdecfc6fff7efffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffdecfc6decfc6ff00ffff00ffff00ffff00ffff00ffff00ff0000ff00ffff00ffff00ffff00ffff00ffff00ffdecfc6decfc6fff7effffffffffffffffffffffffffffffffffffffffff7decfc6decfc6ff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ff0000ff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffdecfc6decfc6decfc6decfc6decfc6decfc6decfc6decfc6ff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ff0000ff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ff0000"))
                e += 1
                rt[a][b][c][d][e].append(Elem("value",text="424d36030000000000003600000028000000100000001000000001001800000000000003000000000000000000000000000000000000ff00ffff00ffff00ffff00fff0eeee6c5f602512133c2b2c2b1719594a4bdcd8d8ff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ff5443453a2525d0c5bdffffffffffffffffffe6e7e8493c3c5e514eb7b1b0ff00ffff00ffff00ffff00ffff00ff5c4a4dc0bbbcffffffffffffffffffffffffffffffffffffffffffd0d0cd584a4dc5bbb8ff00ffff00ffff00ffddd9d9514449ffffffffffffffffffffffff251317251317fffffffffffffffffffffffffffffbd3cfcfff00ffff00ffd9cdc5e0d9daffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff402d30ff00ffefeae6e9e0daffffffffffffffffffffffffffffff251317251317ffffffffffffffffffffffffffffff726361b1aaaad8cbc2ffffffffffffffffffffffffffffffffffff251317251317ffffffffffffffffffffffffffffffffffff332124d7cbc2fffffeffffffffffffffffffffffffffffff251317251317000000ffffffffffffffffffffffffffffff2b1a1dd8cdc4ffffffffffffffffffffffffffffffffffffffffff251317251317ffffffffffffffffffffffffffffff312125d5c8beffffffffffffffffffffffffffffffffffffffffffffffff251317251317ffffffffffffffffffffffff251317d9cdc5feffffffffffffffffffffff000000000000ffffffffffff251317251317ffffffffffffffffffffffff3f3033f5f2f0ded6d1ffffffffffffffffff000000251317251317251317251317000000ffffffffffffffffffb28d89c7c6c6ff00ffcbb6aaffffffffffffffffffffffff000000251317251317000000ffffffffffffffffffffffffb99e9bff00ffff00ffdccbc3e0d6cef2f2f2fffffffffffffffffffffffffffffffffffffffffffffefaffffffe2d4c8f2efeeff00ffff00ffff00fff0ebe6dfd0c9dbcac2f8f7f4fffffffffffffffffffdf8f2e3d9d1cfbfb4ebe3ddff00ffff00ffff00ffff00ffff00ffff00ffff00fffafaf9e1d6ced5c2b9d9c9c2d5c6beddcfc8f4f0efff00ffff00ffff00ffff00ffff00ff"))
                e += 1
                rt[a][b][c][d][e].append(Elem("value"))
                b += 1
                rt[a][b].append(Elem("node",{"oor:name":"com.sun.star.comp.framework.addon","oor:op":"replace"}))
                c = 0
                rt[a][b][c].append(Elem("prop",{"oor:name":"URL","oor:type":"xs:string"})) 
                rt[a][b][c].append(Elem("prop",{"oor:name":"ImageIdentifier","oor:type":"xs:string"}))
                rt[a][b][c].append(Elem("prop",{"oor:name":"Title","oor:type":"xs:string"}))
                rt[a][b][c].append(Elem("prop",{"oor:name":"Target","oor:type":"xs:string"}))      
                d = 0
                rt[a][b][c][d].append(Elem("value",text="org.openoffice.Office.addon.example:Help"))
                d += 1
                rt[a][b][c][d].append(Elem("value")) 
                d += 1
                rt[a][b][c][d].append(Elem("value",{"xml:lang":"x-no-translate"})) 
                rt[a][b][c][d].append(Elem("value",{"xml:lang":"de"},text="Über Add-On Beispiel"))
                rt[a][b][c][d].append(Elem("value",{"xml:lang":"en-US"},text="About Add-On Example"))
                d += 1
                rt[a][b][c][d].append(Elem("value",text="_self"))         
                tree = ET.ElementTree(rt)  # 根要素からxml.etree.ElementTree.ElementTreeオブジェクトにする。
                tree.write(fp.name,"utf-8",True)  # xml_declarationを有効にしてutf-8でファイルに出力する。   
                print("Addons.xcu has been created.")  
if __name__ == "__main__":
    sys.exit(main())