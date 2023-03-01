# -*- codeing = utf-8 -*-
# @Time : 2023/2/23 上午10:34
# @Author : kamitsubaki
# @File : quto.py
# @Software : PyCharm
import os
import chardet
import asyncio
import httpx
import parsel
#####
class opt:
    inputurl = input('URL(要查询的一级域名,例:baidu.com):')
    readlist = str(input('一会生成的list文件名,例list.txt;like:):'))
    url = 'https://api.securitytrails.com/v1/domain/' + inputurl + '/subdomains?children_only=false&include_inactive=false'
    UAheader = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'}
    try:
        with open(readlist,'r') as read_list_readline:
            read_list_readlines = read_list_readline.readlines()
    except:
        pass


def main(readlist,inputurl):
    try:
        o_l_d = os.listdir()
        if readlist in o_l_d:
            search_file = str(input('''检测当前目录下已有此同名文档输入(input number):\n_____________________________\n|[1]内容追加至文档结尾(回车默认Y)|\n|[2]清空文档写入新内容          |\n|[3]重新输入list文件名         |\n|\033[31;40m[4]现成url列表文件，开扫:      \033[0m|\n|[5]不响丸辣，透出脚本          |\n-----------------------------\n'''))
            if search_file == '1' or search_file == '':
                with open(readlist, 'w') as search_file_open:
                    search_file_open.write('./')
                    txtqut(readlist, inputurl,urlb())
            elif search_file == '2':
                txtqut(readlist, inputurl, urlb())
                do_YN = input('是否扫描域名状态:\n[y]扫 (回车默认)\n[n]我不响丸啦，透出！')
                if do_YN.lower() == 'y'.lower() or do_YN == '':
                    asyncio.run(main_httpx(opt.read_list_readlines))
                else:
                    print('------透出成功------')
            elif search_file == '3':
                readlist_re = str(input('一会生成的list文件名,例list.txt;like:):'))
                main(readlist_re, inputurl)
            elif search_file == '4':
                asyncio.run(main_httpx(opt.read_list_readlines))
            elif search_file == '5':
                print('------透出成功------')
            else:
                print('你在干甚魔')
                main(readlist,inputurl)
        else:
            txtqut(readlist,inputurl,urlb())
            do_YN = input('是否扫描域名状态:\n[y]扫 (回车默认)\n[n]我不响丸啦，透出！')
            if do_YN.lower() == 'y'.lower() or do_YN =='':
                asyncio.run(main_httpx(opt.read_list_readlines))
            else:
                print('------透出成功------')

    except Exception as e:
        if hasattr(e,'code'):
            print('------接口%s了------'%e.code)
        elif hasattr(e,'reason'):
            print('------接口%s了------'%e.reason)
        else:
            print('检查下文件里边的是标准格式的列表吗..我没法扫啊')
def urlb():
    APIKEY = input('APIKEY:')
    header = {"accept": "application/json", "APIKEY": APIKEY}
    reqt = httpx.get(url=opt.url, headers=header, timeout=10)
    reqtstr = reqt.read().decode('utf-8')
    list_reqtstr = reqtstr.split('\n')
    return list_reqtstr

def txtqut(readlist,inputurl,list_reqtstr):
    if list_reqtstr != []:
        wl = open(readlist, 'r')
        with open(readlist,'a') as wr:
            for i in list_reqtstr[7:len(list_reqtstr)-2]:
                c = i.replace('"', '').replace(',', '').replace('    ', '').replace('\n', '')
                l = c + '.' + inputurl
                wr.write(l+'\r\n')
            print('all:%d'%(len(wl.readlines())))
    else:
        print('------未获取到域名信息------')
#######################################
def autodecode(content):
    return chardet.detect(content).get("encoding")
#######################################
async def httpx_req(list_url):
    async with httpx.AsyncClient(default_encoding=autodecode,http2=True,headers=opt.UAheader) as client:
        try:
            req_1 = await client.get(url='http://' + list_url,follow_redirects=True)
            selector = parsel.Selector(req_1.text)
            selector_title = selector.xpath('/html/head/title').get().replace('<title>', "").replace('</title>',"").replace('\n',"")
            print(req_1.status_code,'|',selector_title,'|', '\033[33m',list_url.replace('\n',''),'\033[0m', end='\n')
        except Exception as e:
            print('\033[31;40m',req_1.status_code,"|标题获取失败|",list_url.replace('\n',''),'\033[0m', end='\n')
######################################
async def main_httpx(readlines):
    tasklist=[]
    for i in readlines:
        tasklist.append(asyncio.create_task(httpx_req(i.replace('\n',''))))

    await asyncio.wait(tasklist)
########################################################

if __name__ == '__main__':
    main(opt.readlist, opt.inputurl)