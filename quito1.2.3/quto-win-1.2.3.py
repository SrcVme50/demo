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

def main(readlist,inputurl):
    try:
        o_l_d = os.listdir()
        if readlist in o_l_d:
            search_file = str(input('''
    检测当前目录下已有此同名文档
    _____________________________
    |[1]内容追加至文档结尾(回车默认Y)|
    |[2]清空文档写入新内容          |
    |[3]重新输入list文件名         |
    |\033[31;40m[4]现成url列表文件，开扫       \033[0m|
    |[5]不响丸辣，透出脚本          |
    -----------------------------
    输入编号（如:"1"):'''))
            if search_file == '1' or search_file == '':
                txtqut(readlist, inputurl,urlb())
            elif search_file == '2':
                with open(readlist,'w') as re_write:
                    re_write.write('')
                    txtqut(readlist, inputurl, urlb())
                    do_YN = input('是否扫描域名状态:\n[y]扫 (回车默认)\n[n]我不响丸啦，透出！')
                if do_YN.lower() == 'y'.lower() or do_YN == '':
                    with open(readlist, 'r') as read_list_readline:
                        read_list_readlines = read_list_readline.readlines()
                        asyncio.run(main_httpx(read_list_readlines))
                else:
                    print('------透出成功------')
            elif search_file == '3':
                readlist = str(input('一会生成的list文件名,例list.txt;like:):'))
                main(readlist, inputurl)
            elif search_file == '4':
                with open(readlist, 'r') as read_list_readline:
                    read_list_readlines = read_list_readline.readlines()
                    asyncio.run(main_httpx(read_list_readlines))
            elif search_file == '5':
                print('------透出成功------')
            else:
                print('你在干甚魔')
                main(readlist,inputurl)
        else:
            txtqut(readlist,inputurl,urlb())
            do_YN = input('是否扫描域名状态:\n[y]扫 (回车默认)\n[n]我不响丸啦，透出！')
            if do_YN.lower() == 'y'.lower() or do_YN =='':
                with open(readlist, 'r') as read_list_readline:
                    read_list_readlines = read_list_readline.readlines()
                    asyncio.run(main_httpx(read_list_readlines))
            else:
                print('------透出成功------')
    except Exception as e:
        if hasattr(e,'code'):
            print('------接口%s了------'%e.code)
        elif hasattr(e,'reason'):
            print('------接口%s了------'%e.reason)
        else:
            print('检查下文件里边的是标准格式的列表吗..我没法扫啊')
########################
class opt:
    UAheader = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'}
########################
def urlb():
    APIKEY = input('APIKEY:')
    header = {"accept": "application/json", "APIKEY": APIKEY}
    reqt = httpx.get(url=url, headers=header, timeout=10)
    print(url)
    reqtstr = reqt.read().decode('utf-8')
    list_reqtstr = reqtstr.split('\n')
    return list_reqtstr

def txtqut(readlist,inputurl,list_reqtstr):
    if list_reqtstr != []:
        with open(readlist,'a') as wr:
            for i in list_reqtstr[7:len(list_reqtstr)-2]:
                c = i.replace('"', '').replace(',', '').replace('    ', '').replace('\n', '')
                l = c + '.' + inputurl
                wr.write(l+'\r\n')
            with open(readlist, 'r') as wl:
                print('all:%d'%(len(wl.readlines())))
    else:
        print('------未获取到域名信息------')
#######################################
def autodecode(content):
    return chardet.detect(content).get("encoding")
#######################################
async def httpx_req(list_url,req_1_w,):
    async with httpx.AsyncClient(default_encoding=autodecode,http2=True,headers=opt.UAheader,timeout=2) as client:
        try:
            req_1 = await client.get(url='http://' + list_url,follow_redirects=True)
            selector = parsel.Selector(req_1.text)
            selector_title = selector.xpath('/html/head/title').get().replace('<title>', "").replace('</title>',"").replace('\n',"")
            httpx_req_list='%s|%s|%s'%(req_1.status_code,selector_title,list_url.replace('\n',''))
            print(httpx_req_list,end='\n')
            if req_1_w.lower() == 'y'.lower():
                with open(req_1_wfile,'a') as req_w:
                    req_w.write(httpx_req_list+'\r\n')
        except Exception as e:
            try:
                print(req_1.status_code, "|标题获取失败|", list_url.replace('\n', ''), end='\n')
            except Exception as e:
                print("||站点报错||", list_url.replace('\n', ''), end='\n')
######################################
async def main_httpx(readlines):
    httpx_scan = input('''
    (扫描报错的站点,如多次扫描后仍报错,建议手动访问)
    -------------------------
    是否将扫描结果保存到文件中?[Y]写入/[任意键]不保存:''')
    tasklist = []
    if httpx_scan.lower() == 'y'.lower():
        global req_1_wfile
        req_1_wfile=input('保存文件名:')
        if req_1_wfile in os.listdir():
            print('写入文件已存在')
            return
    for i in readlines:
        tasklist.append(asyncio.create_task(httpx_req(i.replace('\n',''),httpx_scan)))

    await asyncio.wait(tasklist)
########################################################

if __name__ == '__main__':
    start_elan = input('''
    -------------------------------
    |[1]获取子域-后扫描域名站点状态    |
    |[2]扫描域名站点状态(已有域名字典) |
    -------------------------------
    输入编号（如:'1'）:''')
    if start_elan == '1':
        inputurl = input('[URL(要查询的一级域名,例:baidu.com)]:')
        readlist = str(input('[一会生成的list文件名,例list.txt)]:'))
        url = 'https://api.securitytrails.com/v1/domain/' + inputurl + '/subdomains?children_only=false&include_inactive=false'
        main(readlist,inputurl)
    elif start_elan == '2':
        try:
            readlist = str(input('''
    [域名list文件名,例list.txt)]:'''))
            with open(readlist, 'r') as read_list_readline:
                read_list_readlines = read_list_readline.readlines()
                asyncio.run(main_httpx(read_list_readlines))
        except Exception as e:
            if 'No such file or directory' in e.args:
                print('\033[35;41m文件错误\033[0m')
            else:
                print('请检查文件内容')
    else:
        print('要不要看看你输入的什么鬼')