# -*- coding: utf-8 -*-
import requests
import io
import sys
import time
import random
import re
import csv
from bs4 import BeautifulSoup

def sendGet(url, headers, cookie='', payload={}, timeout=40):
    s = requests.Session()
    try:
        data = s.get(url, headers=headers, params=payload, timeout=timeout)
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

def extractWrap(card_feed, card_act):
    wrap = []
    # 获取转发、评论、点赞数
    forward = re.sub( "\D", "", card_act.find("a", attrs={"action-type":"feed_list_forward"}).text )  # 找出转发tag，并删除文本中的所有非数字字符
    wrap.append(forward) if forward else wrap.append('0')                                             # 如果转发结果为空串，则写0
    comment = re.sub( "\D", "", card_act.find("a", attrs={"action-type":"feed_list_comment"}).text )
    wrap.append(comment) if comment else wrap.append('0')
    like = card_act.find("a", attrs={"action-type":"feed_list_like"}).find("em").text
    wrap.append(like) if like else wrap.append('0')
    # 获取微博正文文本
    content = card_feed.find("p", attrs={"class":"txt"})
    contentString = ""
    for text in content.strings:
        contentString += text
    wrap.append( contentString.replace(",", "，").strip() ) # 将正文中所有的半角逗号改为全角逗号，避免存储为csv文件后混淆
    return wrap

def timeInc(ori_time):
    parts = [int(num) for num in ori_time.split('-')]
    parts[3] = (parts[3]+1)%24       # 小时数+1
    # 超出零点，天数+1。由于每月的日期是不确定的，因此这里最大只支持逐月搜索。
    if parts[3]==0:
        parts[2] += 1
    # 转str并补零至2位。2020这样4位不受影响。
    newParts = [str(num).zfill(2) for num in parts]
    return '-'.join(newParts)

#浏览器登录后得到的cookie举例，也就是刚才复制的字符串。（请求 URL: https://s.weibo.com/weibo/SK-II?topnav=1&wvr=6&b=1）
# WBtopGlobal_register_version=307744aa77dd5677; _s_tentry=s.weibo.com; Apache=5793306805080.271.1578621230388; 
# SUB=_2A25zE52CDeRhGeNJ7FMS9ynPzjmIHXVQaIhKrDV8PUNbmtANLWbnkW9NS7JzOhCViFuhy6c80otDwjR-1xMFOBvb; UOR=moe.005.tv,widget.weibo.com,www.baidu.com; 
# SINAGLOBAL=703422891379.1595.1512620230601; SCF=Ap-4fMau9nicDJhk_mF3CT5eGn7TLp_IwqZTOy19_8Hu2fsZ0Vb7tAc9H2MiY464HqAUedXXjW1ARyxE2VK_Zis.; 
# ULV=1578621230402:24:2:2:5793306805080.271.1578621230388:1578573567373; SUHB=0QSJppH-T8zEtE; 
# SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWpF6FlAwfOFxEd3eLYeYgc5JpX5K2hUgL.Fo-NS020S0M0SK-2dJLoIEXLxKqL1hnL1K2LxK-LB--LBoqLxKqLBoBL1-zLxK.L1-zLBKnLxKqL1K.LBoBt; 
# login_sid_t=b63dea41a27b7482a818ff3bad35251e; cross_origin_proto=SSL; ALF=1579231313; SSOLoginState=1578626514; un=13507002178; wvr=6; 
# webim_unReadCount=%7B%22time%22%3A1578626549832%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A54%2C%22msgbox%22%3A0%7D

def main():
    i = pageNum = 1
    keyword = '%E6%BE%B3%E5%A4%A7%E5%88%A9%E4%BA%9A'
    timescope = ['2020-01-10-10', '2020-01-10-12']
    curHour = [timescope[0], timeInc(timescope[0])] # 初始化为第一个小时
    headers = { 
        'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.7, ja; q=0.3',
        'Connection': 'Keep-Alive',
        'Cookie': 'SUB=_2A25zJ2K2DeRhGeNJ7FMS9ynPzjmIHXVQVdN-rDV8PUNbmtANLUHRkW9NS7JzOnuVqpRWNT4auHEmUbmizvHXp3o7; SSOLoginState=1579356902; _s_tentry=login.sina.com.cn; Apache=613061983424.1924.1579356906841; UOR=moe.005.tv,widget.weibo.com,www.baidu.com; wvr=6; SINAGLOBAL=703422891379.1595.1512620230601; ALF=1610892902; webim_unReadCount=%7B%22time%22%3A1579356908781%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A59%2C%22msgbox%22%3A0%7D; un=13507002178; SCF=Ap-4fMau9nicDJhk_mF3CT5eGn7TLp_IwqZTOy19_8Hu0ptPZtqut_zzb8_pielEe0bxEmDWG-Dq1zUYLDuOFmA.; ULV=1579356907243:29:7:5:613061983424.1924.1579356906841:1579347386489; SUHB=06Z1b9LckTxkWu; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWpF6FlAwfOFxEd3eLYeYgc5JpX5KzhUgL.Fo-NS020S0M0SK-2dJLoIEXLxKqL1hnL1K2LxK-LB--LBoqLxKqLBoBL1-zLxK.L1-zLBKnLxKqL1K.LBoBt; WBStorage=42212210b087ca50|undefined',
        'Host': 's.weibo.com',
        'Referer': 'https://weibo.com/u/5771377355/home?wvr=5&topnav=1&mod=logo',  # 本字段向服务器表明我是从新浪微博主页过来的
        'Upgrade-Insecure-Requests': '1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'    # 设为Edge浏览器
    }
    url = ''

    with open('weibo.csv', 'w', encoding='utf-8', newline='') as f:         # 创建要写入的文件对象
        csv_writer = csv.writer(f)          # 基于文件对象构建 csv写入对象
        csv_writer.writerow( ["转发","评论","点赞","微博正文"] )             # 构建列表头
        while curHour[1]<=timescope[1]:
            # 遍历当前话题的所有搜索结果页面（因为pageNum会变化，故不能用for只能用while）
            while i<=pageNum:
                if i>1:
                    time.sleep( random.random()*10 )# 等待0~10秒随机时间，防止反爬
                    headers['Referer'] = url        # 若是第二页、第三页等，则将来源页换为上一次的url，防止反爬
                # url字段：xsort=hot 热门微博；timescope=...时间段；page=1 当前页数。
                url = 'https://s.weibo.com/weibo?q='+keyword+'&xsort=hot&suball=1&timescope=custom:'+':'.join(curHour)+'&Refer=SWeibo_box&page='+str(pageNum)
                resp = sendGet(url, headers)        # 注：由于请求头里面已经含有cookies，在requests.get()时不需要重复添加cookies=cookies参数
                soup = BeautifulSoup( resp.content.decode('UTF-8'), 'html.parser' )         # 从响应报文的文本建立bs文档树

                # 第一次访问时要检查当前页是否有符合条件的搜索结果、读取总页数
                if i==1:
                    # 没有结果则会有class为m-error的div元素告知。此时直接结束本次搜索
                    if soup.find("div", attrs={"class":"m-error"}):
                        print("\n>> 时间段"+":".join(curHour)+"没有搜索结果！")
                        break
                    ul = soup.find("ul", attrs={"class":"s-scroll"})
                    pageNum = len( ul.find_all("li") ) if ul else 1                       # 若存在翻页按钮则统计ul下的li个数，否则只有1页
                    print("\n>> 开始抓取时间段"+":".join(curHour)+"的微博，共"+str(pageNum)+"页。")
                
                sys.stdout.write('\r>> 当前处理第'+str(i)+'页……')
                # 获取页面中所有class=card的div节点
                cards = soup.find_all("div", attrs={"class":"card"})
                for card in cards:
                    card_feed = card.find("div", attrs={"class":"card-feed"})     # 检查每个div是否包含feed和act两个子div
                    card_act = card.find("div", attrs={"class":"card-act"})
                    if card_feed and card_act:      # 尝试将其中的所需信息提取出来
                        try:
                            wrap = extractWrap(card_feed, card_act)
                            csv_writer.writerow(wrap)   # 写入csv文件
                        except Exception as e:          # 某一条微博搜索出错则跳过本条
                            print("\n>> 搜索过程出错。",e)
                            continue
                
                i += 1
                #saveToFile(resp.content.decode('UTF-8'), 'weibo_SK-II.txt')
            curHour[0] = timeInc(curHour[0])
            curHour[1] = timeInc(curHour[1])
            i = pageNum = 1
    print("\n>> 抓取完成！")

if __name__ == "__main__":
    main()