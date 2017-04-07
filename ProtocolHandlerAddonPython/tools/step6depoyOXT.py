#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import glob
cwd = os.path.dirname(sys.path[0])  # プロジェクトフォルダの絶対パスを取得。
oxt = glob.glob(os.path.join(cwd,"*.oxt"))  # oxtファイルの絶対パスのリストを取得。
if oxt:
    oxt_path = oxt[0]
    oxt_name = os.path.basename(oxt_path)
    uno_path = os.path.dirname(os.environ["UNO_PATH"])  # programフォルダへのパスを取得。
    unopkg = os.path.join(uno_path,"program","unopkg") 
    args = [unopkg,"add","-f",oxt_path]
    subprocess.run(args) 
    print(os.path.basename(oxt_path) + " has been deployed to " + os.path.basename(uno_path) + ".")
else:
    print("There is no oxt file.")