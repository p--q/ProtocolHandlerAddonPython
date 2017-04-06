#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-

# This name will be rdb file name, .components file name, oxt file name.
BASE_NAME = "ProtocolHandlerAddon_python"  # これがrdbファイル名、.componentsファイル名、oxtファイル名になる。

# tuples of a list of Python UNO Component Files: (file name,service implementation name, service name)
LST = [
    ("ProtocolHandlerAddon.py",'ProtocolHandlerAddonImpl','com.sun.star.frame.ProtocolHandler')
       ]  # (Python UNO Componentファイル名、実装サービス名、サービス名)のタプルのリスト。


