#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import os
import sys
import xml.etree.ElementTree as ET
from settings import BASE_NAME,LST
def createBK(path):  # 引数のファイルがあれば拡張子bkを付ける。
    if os.path.exists(path):  #ファイルがすでに存在するとき。
        bk = path + ".bk"  # バックアップファイル名の取得。
        if os.path.exists(bk): os.remove(bk)  # Windowsの場合は上書きできないので削除が必要。
        os.rename(path, bk)  # 既存のファイルを拡張子bkでバックアップ。 
        print("The previous version of " + os.path.basename(path) + " file has been backuped.")  
def createComponentNode(args):  # Python UNO Component Fileの登録。
    py,IMP_NAME,SEV_NAME = args
    component = ET.Element("component",{'loader': 'com.sun.star.loader.Python',"uri":py})
    implementation = ET.SubElement(component,"implementation",{'name': IMP_NAME})
    service = ET.SubElement(implementation,"service",{'name': SEV_NAME})
    print(py + " is registered in the .components file.")
    return component
def createFileEntry(root,ns,mt,fp):
    return ET.SubElement(root,"{" + ns + "}file-entry",{"{" + ns + "}media-type": mt,"{" + ns + "}full-path" :fp})
def createComponentsFile(src,component_file):  # .componentファイルの作成。
    comp = os.path.join(src,component_file)  # PythonComponent.componentsのパスを取得。
    createBK(comp)  # 引数のファイルがあれば拡張子bkを付ける。
    with open(comp,"w",encoding="utf-8") as f:
        ns = "http://openoffice.org/2010/uno-components"  # 名前空間。
        root = ET.Element("{" + ns + "}components")  # 根の要素を作成。
        for t in LST:  # Python UNO Component Fileの登録。
            root.append(createComponentNode(t))
        tree = ET.ElementTree(root)  # 根要素からxml.etree.ElementTree.ElementTreeオブジェクトにする。
        ET.register_namespace('', ns)  # 名前空間の接頭辞を設定。
        tree.write(f.name,"utf-8",True)  # xml_declarationを有効にしてutf-8でファイルに出力する。   
        print(os.path.basename(f.name) + " has been created.")
def createManifestFile(src,component_file,unordb_file):  # manifext.xmlファイルの作成
    meta = os.path.join(src,"META-INF")  # META-INFフォルダのパスを取得。
    mani = os.path.join(meta,"manifest.xml")  # manifest.xmlのパスを取得。
    if not os.path.exists(meta):  # META-INFフォルダがなければ作成する。
        os.mkdir(meta)
    else:
        createBK(mani)  # 既存のファイルを拡張子bkでバックアップ。  
    with open(mani,"w",encoding="utf-8") as f:
        ns = "http://openoffice.org/2001/manifest"  # 名前空間。
        root = ET.Element("{" + ns + "}manifest")  # 根の要素を作成。
        createFileEntry(root,ns,"application/vnd.sun.star.uno-typelibrary;type=RDB", unordb_file)
        createFileEntry(root,ns,"application/vnd.sun.star.uno-components", component_file)
        tree = ET.ElementTree(root)  # 根要素からxml.etree.ElementTree.ElementTreeオブジェクトにする。
        ET.register_namespace('manifest', ns)  # 名前空間の接頭辞を設定。
        tree.write(f.name,"utf-8",True)  # xml_declarationを有効にしてutf-8でファイルに出力する。   
        print(os.path.basename(f.name) + " has been created.")        
def main():
    component_file = BASE_NAME + ".components"  # .componentsファイル名の作成。
    unordb_file = BASE_NAME + ".uno.rdb"  # rdbファイル名の作成。
    src = os.path.join(os.path.dirname(sys.path[0]),"src")  # srcフォルダの絶対パスを取得。
    createComponentsFile(src,component_file)  # .componentファイルの作成。
    createManifestFile(src,component_file,unordb_file)  # manifext.xmlファイルの作成
if __name__ == "__main__":
    sys.exit(main())    