#!/opt/libreoffice5.2/program/python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import os
import sys
from step1settings import LST,createBK,src_path
import types
class Elem(ET.Element):  
    '''
    キーワード引数textでテキストノードを付加するxml.etree.ElementTree.Element派生クラス。
    '''
    def __init__(self, tag, attrib={},**kwargs):  
        if "text" in kwargs:
            txt = kwargs["text"]
            del kwargs["text"]  
            super().__init__(tag,attrib,**kwargs)
            self._text(txt)
        else:
            super().__init__(tag,attrib,**kwargs)
    def _text(self,txt):
        self.text = txt
class MenuItem(Elem):
    '''
    oor:node-type="MenuItem"を作成するメソッドをもつElemの派生クラス。
    '''
    def createNodes(self,dic,xdic):
        '''
        oor:node-type="MenuItem"のElementのリストを返す。
        
        :param dic: PYTHON_UNO_Component,IMPLE_NAME,SERVICE_NAME,HANDLED_PROTOCOL
        :type dic: dict
        :param xdic: Xml Attributes
        :type xdic: dict
        :returns: a list of nodes
        :rtype: list
        '''
#         ORDER = "URL","Title","ImageIdentifier","Target","Context","Submenu","ControlType","Width"  # ノードは順番が決まっている。 
        ORDER = "URL","Title","Target","Context","Submenu","ControlType","Width"  # ノードは順番が決まっている。 
        lst_nd = list()  # ノードをいれるリスト。
        for key in ORDER:
            if key in xdic:
                val = xdic[key]
                if key == "Title":
                    nd = Elem("prop",{"oor:name":key,"oor:type":"xs:string"})
                    for lang,txt in val.items():
                        nd.append(Elem("value",{"xml:lang":lang},text=txt))
                    lst_nd.append(nd)
                elif key == "Submenu":
                    fn = val.pop()
                    if type(fn) is types.MethodType:
                        lst_nd.append(fn(dic,val))
                else:
                    nd = Elem("prop",{"oor:name":key,"oor:type":"xs:string"})
                    nd.append(Elem("value",text=val)) 
                    lst_nd.append(nd) 
        return lst_nd        
class AddonMenu(MenuItem):
    '''
    Tools->Add-Ons->AddonMenu
    '''
    def __init__(self,dic):
        super().__init__("node",{'oor:name':"AddonMenu"})
        self.append(Elem("node",{'oor:name':dic["HANDLED_PROTOCOL"] + ".function","oor:op":"replace"}))
        self[0].extend(super().createNodes(dic,{"Title":{"en-US":"Add-On example"},"Context":"com.sun.star.text.TextDocument","Submenu":["m1","m2",self.subMenu]}))
    def subMenu(self,dic,val):
        '''
        サブメニューの作成。 
        
        :param dic: PYTHON_UNO_Component,IMPLE_NAME,SERVICE_NAME,HANDLED_PROTOCOL
        :type dic: dict
        :param val: Submenu IDs
        :type val: list
        :returns:  a node for submenu
        :rtype: xml.etree.ElementTree.Element
        
        '''
        nd = Elem("node",{"oor:name":"Submenu"})
        i = 0
        nd.append(Elem("node",{"oor:name":val[i],"oor:op":"replace"}))
        nd[i].extend(super().createNodes(dic,{"URL":dic["HANDLED_PROTOCOL"] + ":Function1","ImageIdentifier":"","Title":{"en-US":"Add-On Function 1"},"Target":"_self"}))
        i += 1
        nd.append(Elem("node",{"oor:name":val[i],"oor:op":"replace"}))
        nd[i].extend(super().createNodes(dic,{"URL":dic["HANDLED_PROTOCOL"] + ":Function2","ImageIdentifier":"","Title":{"en-US":"Add-On Function 2"},"Target":"_self"}))
        return nd
class OfficeMenuBar(MenuItem):
    '''
    OfficeMenuBar
    Main Menu Bar
    
    '''
    def __init__(self,dic):
        super().__init__("node",{'oor:name':"OfficeMenuBar"}) 
        self.append(Elem("node",{'oor:name':dic["HANDLED_PROTOCOL"],"oor:op":"replace"}))   
        self[0].extend(super().createNodes(dic,{"Title":{"en-US":"Add-On example"},"Target":"_self","ImageIdentifier":"","Submenu":["m1","m2","m3",self.subMenu]}))
    def subMenu(self,dic,val):
        nd = Elem("node",{"oor:name":"Submenu"})
        i = 0
        nd.append(Elem("node",{"oor:name":val[i],"oor:op":"replace"}))
        nd[i].extend(super().createNodes(dic,{"URL":dic["HANDLED_PROTOCOL"] + ":Function1","ImageIdentifier":"","Title":{"en-US":"Add-On Function 1"},"Target":"_self","Context":"com.sun.star.text.TextDocument"}))
        i += 1
        nd.append(Elem("node",{"oor:name":val[i],"oor:op":"replace"}))
        nd[i].extend(super().createNodes(dic,{"URL":"private:separator"}))
        i += 1
        nd.append(Elem("node",{"oor:name":val[i],"oor:op":"replace"}))
        nd[i].extend(super().createNodes(dic,{"URL":"","ImageIdentifier":"","Title":{"en-US":"Add-On sub menu"},"Target":"_self","Submenu":["m1",self.subMenu2]}))      
        return nd
    def subMenu2(self,dic,val):
        nd = Elem("node",{"oor:name":"Submenu"})
        i = 0
        nd.append(Elem("node",{"oor:name":val[i],"oor:op":"replace"}))
        nd[i].extend(super().createNodes(dic,{"URL":dic["HANDLED_PROTOCOL"] + ":Function2","ImageIdentifier":"","Title":{"en-US":"Add-On Function 2"},"Target":"_self","Context":"com.sun.star.sheet.SpreadsheetDocument"}))
        return nd
class OfficeToolBar(MenuItem):
    '''
    OfficeToolBar
    View->Toolbars
    Select this tool bar.
    
    ツールバーの名前は設定できない？
    
    '''
    def __init__(self,dic):
        super().__init__("node",{'oor:name':"OfficeToolBar"}) 
        self.append(Elem("node",{'oor:name':dic["HANDLED_PROTOCOL"],"oor:op":"replace"}))  
        self[0].append(Elem("node",{'oor:name':"m1","oor:op":"replace"}))  
        self[0][0].extend(super().createNodes(dic,{"URL":dic["HANDLED_PROTOCOL"] + ":Function1","ImageIdentifier":"","Title":{"en-US":"Function 1"},"Target":"_self","Context":"com.sun.star.text.TextDocument"}))
        self[0].append(Elem("node",{'oor:name':"m2","oor:op":"replace"})) 
        self[0][1].extend(super().createNodes(dic,{"URL":dic["HANDLED_PROTOCOL"] + ":Function2","ImageIdentifier":"","Title":{"en-US":"Function 2"},"Target":"_self","Context":"com.sun.star.text.TextDocument"}))
class Images(MenuItem):
    '''
    Icons
    '''
    def __init__(self,dic):
        super().__init__("node",{'oor:name':"Images"}) 
        name = "com.sun.star.comp.framework.addon.image1"  # ノードを区別するためだけの名前。
        url = dic["HANDLED_PROTOCOL"] + ":Function1"  # アイコンを表示させるコマンドURL
#         dic_image = {
#             "ImageSmall":"",
#             "ImageBig":"",
#             "ImageSmallHC":"",
#             "ImageBigHC":""
#         }
        dic_image = {
            "ImageSmallURL":"%origin%/icons/image1ImageSmall.png",
            "ImageBigURL":"%origin%/icons/image1ImageBig.png",
            "ImageSmallHCURL":"%origin%/icons/image1ImageSmallHC.png",
            "ImageBigHCURL":""
            }
#         dic_image = {18ji
#             "ImageSmall":"%origin%/icons/image1ImageSmall.bmp",
#             "ImageBig":"%origin%/icons/image1ImageBig.bmp",
#             "ImageSmallHC":"%origin%/icons/image1ImageSmallHC.bmp",
#             "ImageBigHC":""
#             }
        self.append(self.userDefinedImages(name,url,dic_image))
        name = "com.sun.star.comp.framework.addon.image2"  # ノードを区別するためだけの名前。
        url = "org.openoffice.Office.addon.example:Help"  # アイコンを表示させるコマンドURL
        dic_image = {
            "ImageSmall":"424d36030000000000003600000028000000100000001000000001001800000000000003000000000000000000000000000000000000ff00ffff00ffff00ffff00fff0eeee6c5f602512133c2b2c2b1719594a4bdcd8d8ff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ff5443453a2525d0c5bdffffffffffffffffffe6e7e8493c3c5e514eb7b1b0ff00ffff00ffff00ffff00ffff00ff5c4a4dc0bbbcfffffffbeadee7bca8e7bcabdfb4a2f1c4b0fffffad0d0cd584a4dc5bbb8ff00ffff00ffff00ffddd9d9514449ffffffd49578b7511eb5582ed29d85ce8b6db54513ba5f32eeccb8fffffffffffbd3cfcfff00ffff00ffd9cdc5e0d9dadc9270ba4613bf511dc99076edeae7f2dcced27b54bc4811ba5724d3ad96ffffff402d30ff00ffefeae6e9e0daeabba4ba4308cb5b28cb5f2ecc7046d99979db8f66ce6635cc5d2dbf4e1ab85225ffeee5726361b1aaaad8cbc2ffffffbf4911c65b21cf6532cc5d2bcc764edbae97dfa284ce6a3bcc5b2bcc602ebb4310d28259ffffff332124d7cbc2fffffebb2600d0703bcc612ecb5b2bca7a56dfd3cdf5f4f1e1a686cd6333ce622dc95e2abe3901ffffff2b1a1dd8cdc4ffffffbe2f00d36f40cb602dcb5928c95a29ce8666e9ded7f1dcd2d77e56cd612acc6530c43a00ffffff312125d5c8beffffffcf3f00d66e3dcc632fc95d2ccb5522c44f19cf8c6becd4ccde9b81d06435d05b26c65619ffffff251317d9cdc5fefffff09361e87437da794ad29a7edfa68ad56f3bd5835bedd5cbe3b399d36939db6126e9b395ffffff3f3033f5f2f0ded6d1fff1e4f9a36ff28b52e3b39beeefedf3e5d9f2e7def4f0eaeba87ee66d2fee9e72fffffcb28d89c7c6c6ff00ffcbb6aaffffffffebdcfec08ff6b584edcebbeddaddf3dfdff5cab3f79c66fbaa7dfce8dcffffffb99e9bff00ffff00ffdccbc3e0d6cef2f2f2fffffcfff2d1fadca3f6cf91fac588fdc68bffe4c5fffefaffffffe2d4c8f2efeeff00ffff00ffff00fff0ebe6dfd0c9dbcac2f8f7f4fffffffffffffffffffdf8f2e3d9d1cfbfb4ebe3ddff00ffff00ffff00ffff00ffff00ffff00ffff00fffafaf9e1d6ced5c2b9d9c9c2d5c6beddcfc8f4f0efff00ffff00ffff00ffff00ffff00ff",
            "ImageBig":"424d560800000000000036000000280000001a0000001a00000001001800000000002008000000000000000000000000000000000000ff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ff0000ff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ff524142524142524142524142524142524142524142524142ff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ff0000ff00ffff00ffff00ffff00ffff00ffff00ff524142524142bda69cd6c7bddecfc6ded7d6e7dfd6e7d7cebdbebdb59694524142524142ff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ff0000ff00ffff00ffff00ffff00ffff00ff524142fffffffffffffffffffffffffffffffffffffffffff7f7f7ffffffffffffffefefbdb6ad524142524142ff00ffff00ffff00ffff00ffff00ffff00ff0000ff00ffff00ffff00ffff00ff524142ffffffffffffffffffefefefdedfdebdb6adc6a694d6a68cdebeade7d7ceefefeff7f7f7ffffffefe7deefe7de524142ff00ffff00ffff00ffff00ffff00ff0000ff00ffff00ffff00ffbda69cffffffffffffffffffefe7ded6a68cbd6139bd5929ce6942c6795abd5929bd5931ce8663debeadefefeffffffffff7f7efe7de524142ff00ffff00ffff00ffff00ff0000ff00ffff00ffff00ffbda69cffffffffffffe7cfc6ce7142bd5929bd5929bd6139d6c7bdffffffd69e84bd5929bd5929bd5929d69e7befefefffffffffefef524142ff00ffff00ffff00ffff00ff0000ff00ffff00ffdecfc6ffffffffffffe7cfc6c66139bd5929c66131ce6131bd7152dedfdeffffffe7c7bdce6131ce6131bd5929bd5929ce8e6befefefffffffdecfc6524142ff00ffff00ffff00ff0000ff00ffff00ffdecfc6ffffffefe7e7ce7142c66131ce6131ce6131ce6131c66131d6a68cefcfbdd68652ce6131ce6131ce6131c66131bd5929d6a68cffffffffffff524142ff00ffff00ffff00ff0000ff00ffdecfc6fff7f7ffffffdeae94bd5929ce6131ce6931ce6131ce6131ce6131ce6939d67142ce6131ce6131ce6131ce6131ce6131bd5929c66139f7dfd6ffffffdecfc6524142ff00ffff00ff0000ff00ffdecfc6fffffff7efefd6714ac66131ce6931ce6931ce6131ce6131c66939debeadffefe7de966bc66131ce6131ce6131ce6131ce6131bd5929deae94ffffffffefe7524142ff00ffff00ff0000ff00ffdecfc6ffffffefd7cece6131ce6931ce6931ce6131ce6131ce6131c66939d6d7d6ffffffdeb69cce6131ce6131ce6131ce6131ce6131bd5929ce8e63f7f7f7ffffff524142ff00ffff00ff0000ff00ffdecfc6ffffffefc7adce6131ce6939ce6931ce6131ce6131ce6131ce6131c6a694f7f7f7fff7efd68e63ce6131ce6131ce6131ce6931ce6131d6714af7efefffffff524142ff00ffff00ff0000ff00ffdecfc6ffffffefc7adce6131d66939ce6931ce6131ce6131ce6131ce6131c66139debeadfffffffff7efd68e63ce6131ce6931ce6931ce6131d6714af7efefffffff524142ff00ffff00ff0000ff00ffdecfc6ffffffffcfb5d67139d67142d66939ce6131ce6131ce6131ce6131ce6131c66939d6c7bdffffffffefefd6714ace6131d66939ce6931d68652fff7f7ffffff524142ff00ffff00ff0000ff00ffdecfc6ffffffffe7dee7794ade7142d67139ce6931ce6131ce6131ce6131ce6131ce6131ce7142f7efefffffffe7ae94ce6131d66939d66939d69673ffffffffffff524142ff00ffff00ff0000ff00ffdecfc6ffffffffffffefa67bef8652de7142d6714adebeadefdfcede9e7bce6131ce6131ce6131f7dfd6ffffffefc7add66939de7142d66939efc7b5ffffffffefef524142ff00ffff00ff0000ff00ffdecfc6f7f7f7ffffffffdfc6f7965af78e5ade794acecfceffffffffefe7d68652ce6131d69e84ffffffffffffdeae94d67139de7142ef9663fff7f7ffffffd6c7bd524142ff00ffff00ff0000ff00ffff00ffdecfc6fffffffffffff7c7adff9e6bf7965ad69e84efefeffffffffffff7ffefdeffffffffffffefe7e7ef9663e7864aef8652f7dfceffffffffffffb59694ff00ffff00ffff00ff0000ff00ffff00ffdecfc6f7f7efffffffffffffffd7adffb684ffa673efb69cdedfdeefefefefefefefefefefe7deefae8cf7965aff9663ffcfb5ffffffffffffdecfc6b59694ff00ffff00ffff00ff0000ff00ffff00ffff00ffdecfc6ffffffffffffffffffffefd6ffdfadffc794ffc794efb69cefb69cffbe9cffb684ffae7bffb68cffe7d6fffffffffffff7efe7bdb6adff00ffff00ffff00ffff00ff0000ff00ffff00ffff00ffff00ffdecfc6fffffffffffffffffffffff7ffffe7ffffd6ffefb5ffefb5ffdfadffdfadffefd6fffff7fffffffffffffff7efdecfc6ff00ffff00ffff00ffff00ffff00ff0000ff00ffff00ffff00ffff00ffff00ffdecfc6fff7efffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffdecfc6decfc6ff00ffff00ffff00ffff00ffff00ffff00ff0000ff00ffff00ffff00ffff00ffff00ffff00ffdecfc6decfc6fff7effffffffffffffffffffffffffffffffffffffffff7decfc6decfc6ff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ff0000ff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffdecfc6decfc6decfc6decfc6decfc6decfc6decfc6decfc6ff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ff0000ff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ff0000",
            "ImageSmallHC":"424d36030000000000003600000028000000100000001000000001001800000000000003000000000000000000000000000000000000ff00ffff00ffff00ffff00fff0eeee6c5f602512133c2b2c2b1719594a4bdcd8d8ff00ffff00ffff00ffff00ffff00ffff00ffff00ffff00ff5443453a2525d0c5bdffffffffffffffffffe6e7e8493c3c5e514eb7b1b0ff00ffff00ffff00ffff00ffff00ff5c4a4dc0bbbcffffffffffffffffffffffffffffffffffffffffffd0d0cd584a4dc5bbb8ff00ffff00ffff00ffddd9d9514449ffffffffffffffffffffffff251317251317fffffffffffffffffffffffffffffbd3cfcfff00ffff00ffd9cdc5e0d9daffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff402d30ff00ffefeae6e9e0daffffffffffffffffffffffffffffff251317251317ffffffffffffffffffffffffffffff726361b1aaaad8cbc2ffffffffffffffffffffffffffffffffffff251317251317ffffffffffffffffffffffffffffffffffff332124d7cbc2fffffeffffffffffffffffffffffffffffff251317251317000000ffffffffffffffffffffffffffffff2b1a1dd8cdc4ffffffffffffffffffffffffffffffffffffffffff251317251317ffffffffffffffffffffffffffffff312125d5c8beffffffffffffffffffffffffffffffffffffffffffffffff251317251317ffffffffffffffffffffffff251317d9cdc5feffffffffffffffffffffff000000000000ffffffffffff251317251317ffffffffffffffffffffffff3f3033f5f2f0ded6d1ffffffffffffffffff000000251317251317251317251317000000ffffffffffffffffffb28d89c7c6c6ff00ffcbb6aaffffffffffffffffffffffff000000251317251317000000ffffffffffffffffffffffffb99e9bff00ffff00ffdccbc3e0d6cef2f2f2fffffffffffffffffffffffffffffffffffffffffffffefaffffffe2d4c8f2efeeff00ffff00ffff00fff0ebe6dfd0c9dbcac2f8f7f4fffffffffffffffffffdf8f2e3d9d1cfbfb4ebe3ddff00ffff00ffff00ffff00ffff00ffff00ffff00fffafaf9e1d6ced5c2b9d9c9c2d5c6beddcfc8f4f0efff00ffff00ffff00ffff00ffff00ff",
            "ImageBigHC":""
            }
#         dic_image = {
#             "ImageSmall":"",
#             "ImageBig":"",
#             "ImageSmallHC":"",
#             "ImageBigHC":""
#             }
        self.append(self.userDefinedImages(name,url,dic_image))
    def userDefinedImages(self,name,url,dic_image):  
        '''
        アイコンの設定。
        
        :param name: name of icon
        :type name: str
        :param url: uri of icon
        :type url: str
        :param dic_image:  a dictionary of the same image with different sizes
        :type dic_image: dict
        :returns: a node for an image
        :rtype: xml.etree.ElementTree.Element
        '''
        nd = Elem("node",{"oor:name":name,"oor:op":"replace"})
        nd.append(Elem("prop",{"oor:name":"URL"}))
        nd[0].append(Elem("value",text=url))
        nd.append(Elem("node",{"oor:name":"UserDefinedImages"}))
        ORDER = "ImageSmall","ImageBig","ImageSmallHC","ImageBigHC"
        for key in ORDER:
            if key in dic_image:
                snd = Elem("prop",{"oor:name":key,"oor:type":"xs:hexBinary"})
                snd.append(Elem("value",text=dic_image[key]))
                nd[1].append(snd)
        ORDER = "ImageSmallURL","ImageBigURL"  # "ImageSmallHC","ImageBigHC"があるとなぜか画像が表示されない。
        for key in ORDER:
            if key in dic_image:
                snd = Elem("prop",{"oor:name":key,"oor:type":"xs:string"})
                snd.append(Elem("value",text=dic_image[key]))
                nd[1].append(snd)        
        return nd
class OfficeHelp(MenuItem):   
    '''
    Help
    '''
    def __init__(self,dic):
        super().__init__("node",{'oor:name':"OfficeHelp"}) 
        self.append(Elem("node",{'oor:name':"com.sun.star.comp.framework.addon","oor:op":"replace"}))           
        self[0].extend(super().createNodes(dic,{"URL":dic["HANDLED_PROTOCOL"] + ":Help","ImageIdentifier":"","Title":{"x-no-translate":"","de":"Über Add-On Beispiel","en-US":"About Add-On Example"},"Target":"_self"}))
def main():
    #Creation of ProtocolHandler.xcu
    os.chdir(src_path)  # srcフォルダに移動。
    for dic in LST:  # 設定リストの各辞書について
        if "HANDLED_PROTOCOL" in dic:  # HANDLED_PROTOCOLが辞書のキーにあるとき
            filename =  "ProtocolHandler.xcu"
            createBK(filename)  # すでにあるファイルをbkに改名
            with open(filename,"w",encoding="utf-8") as fp:
                rt = Elem("oor:component-data",{"oor:name":"ProtocolHandler","oor:package":"org.openoffice.Office","xmlns:oor":"http://openoffice.org/2001/registry","xmlns:xs":"http://www.w3.org/2001/XMLSchema","xmlns:xsi":"http://www.w3.org/2001/XMLSchema-instance"})  # 根の要素を作成。
                rt.append(Elem("node",{'oor:name':"HandlerSet"}))
                rt[0].append(Elem("node",{'oor:name':dic["IMPLE_NAME"],"oor:op":"replace"}))
                rt[0][0].append(Elem("prop",{'oor:name':"Protocols","oor:type":"oor:string-list"}))
                rt[0][0][0].append(Elem("value",text = dic["HANDLED_PROTOCOL"] + ":*"))
                tree = ET.ElementTree(rt)  # 根要素からxml.etree.ElementTree.ElementTreeオブジェクトにする。
                tree.write(fp.name,"utf-8",True)  # xml_declarationを有効にしてutf-8でファイルに出力する。   
                print(filename + " has been created.")    
            #Creation of Addons.xcu
            filename =  "Addons.xcu"
            createBK(filename)  # すでにあるファイルをbkに改名
            with open(filename,"w",encoding="utf-8") as fp:   
                rt = Elem("oor:component-data",{"oor:name":"Addons","oor:package":"org.openoffice.Office","xmlns:oor":"http://openoffice.org/2001/registry","xmlns:xs":"http://www.w3.org/2001/XMLSchema"})  # 根の要素を作成。
                rt.append(Elem("node",{'oor:name':"AddonUI"}))
                rt[0].extend([AddonMenu(dic),OfficeMenuBar(dic),OfficeToolBar(dic),Images(dic),OfficeHelp(dic)])
                tree = ET.ElementTree(rt)  # 根要素からxml.etree.ElementTree.ElementTreeオブジェクトにする。
                tree.write(fp.name,"utf-8",True)  # xml_declarationを有効にしてutf-8でファイルに出力する。   
                print(filename + " has been created.")  
if __name__ == "__main__":
    sys.exit(main())