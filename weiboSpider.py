# -*- coding: utf-8 -*-
import requests
import io
import sys
import time
import random
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8') #改变标准输出的默认编码

def sendGet(url, headers, cookie=''):
    s = requests.Session()
    try:
        data = s.get(url, headers=headers)
    except Exception as e:
        print(e)
        return None
    return data

def saveToFile(text, outPath='output.txt', head=""):
    with open('./'+outPath,'w',encoding='utf-8') as f:
        if head:
            f.write( "#"+str(head)+"\n" )
        f.write(text)
        print(">> 内容已保存在","./"+outPath)
    return True

#浏览器登录后得到的cookie，也就是刚才复制的字符串
# 请求 URL: https://s.weibo.com/weibo/SK-II?topnav=1&wvr=6&b=1
# WBtopGlobal_register_version=307744aa77dd5677; _s_tentry=s.weibo.com; Apache=5793306805080.271.1578621230388; 
# SUB=_2A25zE52CDeRhGeNJ7FMS9ynPzjmIHXVQaIhKrDV8PUNbmtANLWbnkW9NS7JzOhCViFuhy6c80otDwjR-1xMFOBvb; UOR=moe.005.tv,widget.weibo.com,www.baidu.com; 
# SINAGLOBAL=703422891379.1595.1512620230601; SCF=Ap-4fMau9nicDJhk_mF3CT5eGn7TLp_IwqZTOy19_8Hu2fsZ0Vb7tAc9H2MiY464HqAUedXXjW1ARyxE2VK_Zis.; 
# ULV=1578621230402:24:2:2:5793306805080.271.1578621230388:1578573567373; SUHB=0QSJppH-T8zEtE; 
# SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWpF6FlAwfOFxEd3eLYeYgc5JpX5K2hUgL.Fo-NS020S0M0SK-2dJLoIEXLxKqL1hnL1K2LxK-LB--LBoqLxKqLBoBL1-zLxK.L1-zLBKnLxKqL1K.LBoBt; 
# login_sid_t=b63dea41a27b7482a818ff3bad35251e; cross_origin_proto=SSL; ALF=1579231313; SSOLoginState=1578626514; un=13507002178; wvr=6; 
# webim_unReadCount=%7B%22time%22%3A1578626549832%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A54%2C%22msgbox%22%3A0%7D

# 请求 URL: https://s.weibo.com/weibo?q=%E5%AE%9D%E6%B4%81&wvr=6&b=1&Refer=SWeibo_box
# WBtopGlobal_register_version=307744aa77dd5677; _s_tentry=s.weibo.com; Apache=5793306805080.271.1578621230388; 
# SUB=_2A25zE52CDeRhGeNJ7FMS9ynPzjmIHXVQaIhKrDV8PUNbmtANLWbnkW9NS7JzOhCViFuhy6c80otDwjR-1xMFOBvb; 
# login_sid_t=b63dea41a27b7482a818ff3bad35251e; cross_origin_proto=SSL; SSOLoginState=1578626514; UOR=moe.005.tv,widget.weibo.com,www.baidu.com; wvr=6; 
# SINAGLOBAL=703422891379.1595.1512620230601; ALF=1579231313; 
# webim_unReadCount=%7B%22time%22%3A1578626549832%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A54%2C%22msgbox%22%3A0%7D; un=13507002178; 
# SCF=Ap-4fMau9nicDJhk_mF3CT5eGn7TLp_IwqZTOy19_8Hu2fsZ0Vb7tAc9H2MiY464HqAUedXXjW1ARyxE2VK_Zis.; 
# ULV=1578621230402:24:2:2:5793306805080.271.1578621230388:1578573567373; SUHB=0QSJppH-T8zEtE; 
# SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWpF6FlAwfOFxEd3eLYeYgc5JpX5K2hUgL.Fo-NS020S0M0SK-2dJLoIEXLxKqL1hnL1K2LxK-LB--LBoqLxKqLBoBL1-zLxK.L1-zLBKnLxKqL1K.LBoBt
#cookie_str = r'PHPSESSID=9f20c6bb676841f38aee8589aceb5c7f; username=zhonghuihong; password=XXX'
#cookies = {}   #把cookie字符串处理成字典，以便接下来使用
#for line in cookie_str.split(';'):
#    key, value = line.strip().split('=', 1)
#    cookies[key] = value
#print(cookies)

def main():
    url = 'https://s.weibo.com/weibo/SK-II?topnav=1&wvr=6&b=1'
    headers = { 
        'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.7, ja; q=0.3',
        'Connection': 'Keep-Alive',
        'Cookie': 'WBtopGlobal_register_version=307744aa77dd5677; WBStorage=42212210b087ca50|undefined; _s_tentry=s.weibo.com; Apache=5793306805080.271.1578621230388; SUB=_2A25zE52CDeRhGeNJ7FMS9ynPzjmIHXVQaIhKrDV8PUNbmtANLWbnkW9NS7JzOhCViFuhy6c80otDwjR-1xMFOBvb; login_sid_t=b63dea41a27b7482a818ff3bad35251e; cross_origin_proto=SSL; SSOLoginState=1578626514; UOR=moe.005.tv,widget.weibo.com,www.baidu.com; wvr=6; SINAGLOBAL=703422891379.1595.1512620230601; ALF=1579231313; webim_unReadCount=%7B%22time%22%3A1578626549832%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A54%2C%22msgbox%22%3A0%7D; un=13507002178; SCF=Ap-4fMau9nicDJhk_mF3CT5eGn7TLp_IwqZTOy19_8Hu2fsZ0Vb7tAc9H2MiY464HqAUedXXjW1ARyxE2VK_Zis.; ULV=1578621230402:24:2:2:5793306805080.271.1578621230388:1578573567373; SUHB=0QSJppH-T8zEtE; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWpF6FlAwfOFxEd3eLYeYgc5JpX5K2hUgL.Fo-NS020S0M0SK-2dJLoIEXLxKqL1hnL1K2LxK-LB--LBoqLxKqLBoBL1-zLxK.L1-zLBKnLxKqL1K.LBoBt',
        'Host': 's.weibo.com',
        'Referer': 'https://weibo.com/u/5771377355/home?wvr=5&topnav=1&mod=logo',  # 本字段向服务器表明我是从新浪微博主页过来的
        'Upgrade-Insecure-Requests': '1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'    # 设为Edge浏览器
    }
    # 一：请求头header是不是必须要加
    # ①、防止封ip，加上准没错
    # ②、反制反爬机制，（headers是解决requests请求反爬的方法之一，相当于我们进去这个网页的服务器本身，假装自己本身在访问网页）
    # 二：请求头里面已经含有cookies,在requests.get()时不需要重复添加cookies=cookies参数
    resp = sendGet(url, headers)
    #time.sleep( random.random()*3 )
    soup = BeautifulSoup( resp.content.decode('UTF-8'), 'html.parser' )
    print(soup)
    saveToFile(resp.content.decode('UTF-8'), 'weibo_SK-II.txt')
    '''soup_table=soup.find(attrs={'class':'table table-striped table-bordered table-hover'});
    #print(soup_table);
    soup_str=soup_table.findAll(attrs={'style':'text-align:center;vertical-align:middle;word-break:break-all; word-wrap:break-all;'});
    print(soup_str);
    #for each in soup_str:
    #print(each.string);
    #book_div = soup.find(attrs={"id":"book"})
    #book_a = book_div.findAll(attrs={"class":"title"})
    #for book in book_a:
    #print book.string
    #print(soup);'''

if __name__ == "__main__":
    main()