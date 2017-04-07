#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-

# This name will be rdb file name, .components file name, oxt file name.
BASE_NAME = "ProtocolHandlerAddonPython"  # これがrdbファイル名、.componentsファイル名、oxtファイル名になる。

# tuples of a list of Python UNO Component Files: (file name,service implementation name, service name,handled protocol)
LST = [
    {PYTHON_UNO_Component:"ProtocolHandlerAddon.py",IMPLE_NAME:'ProtocolHandlerAddonImpl',SERVICE_NAME:'com.sun.star.frame.ProtocolHandler',HANDLED_PROTOCOL:"org.openoffice.Office.addon.example" }
       ]  # (Python UNO Componentファイル名、実装サービス名、サービス名,プロトコール名)のタプルのリスト。
