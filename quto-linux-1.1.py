# -*- codeing = utf-8 -*-
# @Time : 2023/2/23 上午10:34
# @Author : kamitsubaki
# @File : quto.py
# @Software : PyCharm
# import urllib.request
#
inputurl = input('URL(要查询的一级域名,例:baidu.com):')
readlist = input('一会生成的list文件名\n(tip:填写现有文档，将会于文档内容末尾追加\n;例list.txt;like:):')
APIKEY = input('APIKEY:')

url = 'https://api.securitytrails.com/v1/domain/' + inputurl + '/subdomains?children_only=false&include_inactive=false'


header = {"accept": "application/json", "APIKEY": APIKEY}

try:
    list_reqtstr = []
    req = urllib.request.Request(url=url, headers=header, method='GET')
    reqt = urllib.request.urlopen(req, timeout=10)
    reqtstr = reqt.read().decode('utf-8')
    list_reqtstr = reqtstr.split('\n')
except Exception as e:
     print(e)

def txtqut(readlist,inputurl):
    try:
        wr = open(readlist,'a')
        wl = open(readlist,'r')
        for i in list_reqtstr[7:len(list_reqtstr) - 2]:
            c = i.replace('"', '').replace(',', '').replace('    ', '').replace('\n', '')
            l = c + '.' + inputurl
            wr.write(l+'\n')
        wr.close()
        print('all:%d'%(len(wl.readlines())))
        wl.close()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    txtqut(readlist, inputurl)