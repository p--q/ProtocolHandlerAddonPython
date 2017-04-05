#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import sys
from xml.etree.ElementTree import Element as Elem
def main():
    src = os.path.join(os.path.dirname(sys.path[0]),"src")  # srcフォルダの絶対パスを取得。
    #Creation of ProtocolHandler.xcu
    protocolhandler = os.path.join(src,"ProtocolHandler.xcu")
    with open(protocolhandler,"w",encoding="utf-8") as f:
        root = ET.Element("oor:component-data",{"oor:name":"ProtocolHandler","oor:package":"org.openoffice.Office","xmlns:oor":"http://openoffice.org/2001/registry","xmlns:xs":"http://www.w3.org/2001/XMLSchema","xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"})  # 根の要素を作成。
        HandlerSet = ET.SubElement(root,"node",{'oor:name':"HandlerSet"})
        Impl =  ET.SubElement(HandlerSet,"node",{'oor:name':"ProtocolHandlerAddon$ProtocolHandlerAddonImpl","oor:op":"replace"})
        Protocols = ET.SubElement(Impl,"prop",{'oor:name':"Protocols","oor:type":"oor:string-list"})
        ET.SubElement(Protocols,"value").text = "org.openoffice.Office.addon.example:*"
        tree = ET.ElementTree(root)  # 根要素からxml.etree.ElementTree.ElementTreeオブジェクトにする。
        tree.write(f.name,"utf-8",True)  # xml_declarationを有効にしてutf-8でファイルに出力する。   
        print("ProtocolHandler.xcu has been created.")  
     #Creation of Addons.xcu
    addons = os.path.join(src,"Addons.xcu")    
    with open(addons,"w",encoding="utf-8") as f:   
        rt = Elem("oor:component-data",{"oor:name":"Addons","oor:package":"org.openoffice.Office","xmlns:oor":"http://openoffice.org/2001/registry","xmlns:xs":"http://www.w3.org/2001/XMLSchema"})  # 根の要素を作成。
        rt.append(Elem("node",{'oor:name':"AddonUI"}))
        rt[0].append(Elem("node",{'oor:name':"AddonMenu"}))
        rt[0].append(Elem("node",{'oor:name':"OfficeMenuBar"}))
        rt[0].append(Elem("node",{'oor:name':"OfficeToolBar"}))
        rt[0].append(Elem("node",{'oor:name':"Images"}))
        rt[0].append(Elem("node",{'oor:name':"OfficeHelp"}))
        rt[0][0].append(Elem("node",{"oor:name":"org.openoffice.Office.addon.example.function","oor:op":"replace"}))
        rt[0][0][0].append(Elem("prop",{"oor:name":"Title","oor:type":"xs:string"}))
        rt[0][0][0].append(Elem("prop",{"oor:name":"Context","oor:type":"xs:string"}))
        rt[0][0][0].append(Elem("node",{"oor:name":"Submenu"}))                                      
        rt[0][0][0][0].append(Elem("value",{"xml:lang":"en-US"}))
        rt[0][0][0][0][0].text = "Add-On example"
        rt[0][0][0][1].append(Elem("value"))
        rt[0][0][0][1][0].text = "com.sun.star.text.TextDocument"
        rt[0][0][0][2].append(Elem("node",{"oor:name":"m1","oor:op":"replace"})) 
        rt[0][0][0][2][0].append(Elem("prop",{"oor:name":"URL","oor:type":"xs:string"})) 
        rt[0][0][0][2][0].append(Elem("prop",{"oor:name":"ImageIdentifier","oor:type":"xs:string"}))
        rt[0][0][0][2][0].append(Elem("prop",{"oor:name":"Title","oor:type":"xs:string"}))
        rt[0][0][0][2][0].append(Elem("prop",{"oor:name":"Target","oor:type":"xs:string"}))
        
       
       
       
       
       
       

        tree = ET.ElementTree(rt)  # 根要素からxml.etree.ElementTree.ElementTreeオブジェクトにする。
        tree.write(f.name,"utf-8",True)  # xml_declarationを有効にしてutf-8でファイルに出力する。   
        print("Addons.xcu has been created.")  
if __name__ == "__main__":
    sys.exit(main())