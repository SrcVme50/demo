# -*- codeing = utf-8 -*-
# @Time : 2023/2/23 上午10:34
# @Author : kamitsubaki
# @File : quto.py
# @Software : PyCharm
import urllib.request

inputurl = input('URL(要查询的一级域名,例:baidu.com):')
readlist = input('一会生成的list文件名(,like:list.txt):')
APIKEY = input('APIKEY:')

url = 'https://api.securitytrails.com/v1/domain/' + inputurl + '/subdomains?children_only=false&include_inactive=false'

header = {"accept": "application/json", "APIKEY": APIKEY}



def wj(reqtstr):
    global listrb
    try:
        listw.write(reqtstr)
        listw.close()
        listrb=listr.readlines()
    except Exception as E:
        print(E)

def txtqut(readlist,inputurl):
    for i in listrb[7:len(listrb) - 2]:
        c = i.replace('"', '').replace(',', '').replace('    ', '').replace('\n', '')
        l = c + '.' + inputurl
        open(readlist,'a').write(l+'\n')

if __name__ == '__main__':
    try:
        req = urllib.request.Request(url=url, headers=header, method='GET')
        reqt = urllib.request.urlopen(req, timeout=10)
        reqtstr = reqt.read().decode('utf-8')
        listw = open('dolist.txt', 'w')
        listr = open('dolist.txt', 'r')
        wj(reqtstr)
        txtqut(readlist, inputurl)
    except Exception as e:
        print(e)
