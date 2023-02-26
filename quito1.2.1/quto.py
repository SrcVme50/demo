# -*- codeing = utf-8 -*-
# @Time : 2023/2/23 上午10:34
# @Author : kamitsubaki
# @File : quto.py
# @Software : PyCharm
import os
import urllib.request

class opt:
    inputurl = input('URL(要查询的一级域名,例:baidu.com):')
    readlist = str(input('一会生成的list文件名,例list.txt;like:):'))
    APIKEY = input('APIKEY:')
    url = 'https://api.securitytrails.com/v1/domain/' + inputurl + '/subdomains?children_only=false&include_inactive=false'
    header = {"accept": "application/json", "APIKEY": APIKEY}

def main(readlist,inputurl):
    try:
        o_l_d = os.listdir()
        if readlist in o_l_d:
            search_file = str(input('检测当前目录下已有此同名文档输入(input number):\n[1]内容追加至文档结尾(回车默认Y)\n[2]清空文档写入新内容\n[3]重新输入list文件名\n[4]不响丸辣，透出脚本\n'))
            if search_file == '1' or search_file == '':
                with open(readlist, 'w') as search_file_open:
                    search_file_open.write('./')
                    txtqut(readlist, inputurl,urlb())
            elif search_file == '2':
                txtqut(readlist, inputurl,urlb())
            elif search_file == '3':
                readlist_re = str(input('一会生成的list文件名,例list.txt;like:):'))
                main(readlist_re, inputurl)
            elif search_file == '4':
                print('------透出成功------')
            else:
                print('你在干甚魔')
                main(readlist,inputurl)
        else:
            txtqut(readlist,inputurl,urlb())
    except Exception as e:
        if hasattr(e,'code'):
            print('------接口%s了------'%e.code)
        elif hasattr(e,'reason'):
            print('------接口%s了------'%e.reason)
        else:
            print('------接口%s------'%e)
def urlb():
    req = urllib.request.Request(url=opt.url, headers=opt.header, method='GET')
    reqt = urllib.request.urlopen(req, timeout=10)
    reqtstr = reqt.read().decode('utf-8')
    list_reqtstr = reqtstr.split('\n')
    return list_reqtstr

def txtqut(readlist,inputurl,list_reqtstr):
    if list_reqtstr != []:
        wl = open(readlist, 'r')
        with open(readlist,'a') as wr:
            for i in list_reqtstr[7:len(list_reqtstr)-2]:
                print(i)
                c = i.replace('"', '').replace(',', '').replace('    ', '').replace('\n', '')
                l = c + '.' + inputurl
                wr.write(l+'\n')
            print('all:%d'%(len(wl.readlines())))
    else:
        print('------未获取到域名信息------')

if __name__ == '__main__':
    main(opt.readlist, opt.inputurl)