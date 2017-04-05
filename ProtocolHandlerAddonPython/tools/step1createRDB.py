#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import sys
import os
import glob
from itertools import chain
import subprocess
from settings import BASE_NAME
def main():
    unordb_file = BASE_NAME + ".uno.rdb"
    # 各々のパスの取得。
    src = os.path.join(os.path.dirname(sys.path[0]),"src")  # srcフォルダの絶対パスを取得。
    uno_path = os.environ["UNO_PATH"]  # programフォルダへの絶対パスを取得。
    regmerge = os.path.join(uno_path,"regmerge")  # regmergeの絶対パスを取得。
    sdk_path = os.path.join(os.path.dirname(uno_path),"sdk")  # SDKフォルダへの絶対パスを取得。
    idlc = os.path.join(sdk_path,"bin","idlc")  # idlcの絶対パスを取得。
    regview = os.path.join(uno_path,"regview")  # regviewの絶対パスを取得。
    idl = os.path.join(sdk_path,"idl")  # SDKのidlフォルダへの絶対パスを取得。
    myidl = os.path.join(src,"idl")  # PyDevプロジェクトのidlフォルダへの絶対パスを取得。
    #myidlフォルダがなければmyidlフォルダを作成して終わる。
    if not os.path.exists(myidl):
        os.mkdir(myidl)
        print("Please create idl files in the idl folder.")
        sys.exit()
    #すべての存在確認をする。ツールがそろっていなければ終了する。
    for p in [regmerge,idlc,regview,idl]:
        if not os.path.exists(p):
            print(p + " does not exit.")
            sys.exit()
    urdsp = os.path.join(myidl,"*.urd")  # globで取得するためのurdファイルの絶対パスを作成。
    for i in glob.iglob(urdsp):  # すでにあるurdファイルを削除。
        os.remove(i)
    for i in glob.iglob(os.path.join(myidl,"*.idl")):  # 各idlファイルをidlcでコンパイル。
        args = [idlc,"-I" + myidl,"-I" + idl, "-O" + myidl, i]
        subprocess.run(args)
    rdb = os.path.join(src,unordb_file)  # uno.rdbファイルの絶対パスを取得。
    urds = glob.glob(urdsp)  # urdファイルのリストを取得。
    if not urds:  # urdファイルが出力されていないとき
        print("urd files are not created.")
        sys.exit()
    args = [regmerge,rdb,"/UCR"]   # mergeKeyName /UCR(UNO core reflection)も追加してurdファイルをuno.rdbファイルにまとめる。
    args.extend(urds)
    subprocess.run(args)
    for i in urds:  # 使用済みurdファイルを削除。
        os.remove(i)
    if os.path.exists(rdb):  # rdbファイルができていれば、
        args = [regview,rdb]
        subprocess.run(args)  # rdbファイルの中身を出力。
        print(unordb_file + " creation succeeded.")
    else:
        print("Failed to create " + unordb_file + ".")
if __name__ == "__main__":
    sys.exit(main())