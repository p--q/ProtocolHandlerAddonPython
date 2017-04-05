#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import sys
def main():
    src = os.path.join(os.path.dirname(sys.path[0]),"src")  # srcフォルダの絶対パスを取得。
    #Creation of ProtocolHandler.xcu
    prot = os.path.join(src,"ProtocolHnadler.xcu")
    with open(prot,"w",encoding="utf-8") as f:
        oor="http://openoffice.org/2001/registry"  # 名前空間。
        ET.register_namespace('oor', oor)  # 名前空間の接頭辞を設定。
        ET.register_namespace('xs', "http://www.w3.org/2001/XMLSchema")  # 名前空間の接頭辞を設定。
        ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")  # 名前空間の接頭辞を設定。
        root = ET.Element("{" + oor + "}component-data",{"{" + oor + "}name":"ProtocolHandler","{" + oor + "}package":"org.openoffice.Office"})  # 根の要素を作成。
        
        
        
        
#         createFileEntry(root,ns,"application/vnd.sun.star.uno-typelibrary;type=RDB", unordb_file)
#         createFileEntry(root,ns,"application/vnd.sun.star.uno-components", component_file)
        tree = ET.ElementTree(root)  # 根要素からxml.etree.ElementTree.ElementTreeオブジェクトにする。
        tree.write(f.name,"utf-8",True)  # xml_declarationを有効にしてutf-8でファイルに出力する。   
        print("ProtocolHandler.xcu has been created.")  





if __name__ == "__main__":
    sys.exit(main())