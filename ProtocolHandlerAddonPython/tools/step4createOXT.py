#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
from settings import BASE_NAME
from createManifest import createBK
import subprocess
import glob
import os
import shutil
import sys
from itertools import chain
def main():
    pro = src = os.path.dirname(sys.path[0])  # プロジェクトフォルダの絶対パスを取得。
    oxt = os.path.join(pro,BASE_NAME + ".oxt")  # 作成するoxtファイルの絶対パスを取得。
    createBK(oxt)  # すでにあるoxtファイルをbkに改名。
    os.chdir(os.path.join(pro,"src"))  # 作業ディレクトリをsrcに変更。
    if not shutil.which("zip"):  # zipコマンドの有効を確認。
        print("The zip command must be valid for execution.")
        sys.exit()
    mani = glob.glob(os.path.join("META-INF","manifest.xml"))  # manifest.xmlの絶対パスを取得。
    rdbs = glob.glob("*.rdb")  # rdbファイルの絶対パスを取得。
    comps = glob.glob("*.components")  # .componentsファイルの絶対パスを取得。 
    pys = glob.glob("*.py")  # Python UNO Componentファイルの絶対パスを取得。 
    files = mani,rdbs,comps,pys  # glob.globで取得したファイルリストのタプル。
    if not all(files):  # いずれかのファイルが欠けているとき。
        names = "manifext.xml","*.rdb","*.components","*.py"
        for i,f in enumerate(files):  # 必須ファイルの存在確認。
            if not f:  # ファイルが欠けている時
                print(names[i] + "does not exist.")
                sys.exit()
    args = ["zip",oxt]
    args.extend(chain.from_iterable(files))
    subprocess.run(args)  # 必須ファイルをoxtファイルに収納。
    if os.path.exists("pythonpath"):  # pythonpathフォルダがあるとき
        exts = "py","mo"  # oxtファイルに含めるファイルの拡張子のタプル。
        files = []  # ファイルリストの初期化。
        for ext in exts:
            g = glob.glob(os.path.join("pythonpath","**","*." + ext),recursive=True)  # 指定拡張子のファイルのパスを取得。
            if g: files.extend(g)  # 指定拡張子のファイルがあるのならリストに追加。
        if not g:
            args = ["zip","-u",oxt]
            args.extend(files)
            subprocess.run(args)  # pythonpathフォルダをoxtファイルに収納。
if __name__ == "__main__":
    sys.exit(main())
    