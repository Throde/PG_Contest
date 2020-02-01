# -*- coding: utf-8 -*-
import requests
import re
import json
import csv
import time
import random
import sys
from bs4 import BeautifulSoup
from weiboSpider import saveToFile, sendGet

def parseBracket(text, trigger="[", num=1):
    '''对于含有多层嵌套的字符串，找出其最大层的括号中的文本（连端括号）并返回。
        trigger是最外层的左括号，num是最大层并列的个数。若num>1，则以列表形式返回。'''
    stack = []      # 辅助栈
    index = text.find(trigger)
    if index == -1:
        return ""
    contents = []
    length = len(text)
    startIndx = index
    cnt = 0
    while cnt<num:
        while index < length:
            if text[index] in ("{", "[", "("):      # 左括号入栈
                stack.append( text[index] )
            elif text[index] in ("}", "]", ")"):    # 右括号出栈
                stack.pop()
            if not stack:
                break
            index += 1
        contents.append( text[startIndx:index+1] )
        # 浮标右移至下一匹配处，继续寻找
        index = startIndx = text.find(trigger, index+1)
        if startIndx == -1:
            break
        cnt += 1
    return contents

def main(keyword='%E8%88%92%E8%82%A4%E4%BD%B3%E6%B4%97%E6%89%8B%E6%B6%B2'):
    i = pageNum = 1
    keyword = input(">> 请输入搜索关键词（复制URL中的转码结果）：")  # 可以为各种商品名称（手工转码后）
    headers={    
            'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.7, ja; q=0.3',
            'Cache-Control': 'max-age=0',
            'Cookie': 'enc=Ua5usRIyWoZGZPq%2F24sc3QDLNNNg10CAxzfwjMrNNwRDIEP77I%2F3PxnMOtaAXblPBGoVx92Mri138Y9s00e91Q%3D%3D; uc4=id4=0%40U22GVfBGFOM6l7ocHkmNAOgBD2ga&nk4=0%40r7q0tQvWOx4NB3n0E47%2BxjwEgRCnh44keMuqxZXWeA%3D%3D; _cc_=URm48syIZQ%3D%3D; isg=BCsr6e288VF5LC0xuah1-i02o08VQD_Cy1P6952pGmrBPEqeABF5Eqn-kvxSB5e6; thw=cn; uc3=nk2=rUsy40agieA1CAZiZZatPafMds0%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D&vt3=F8dBxdkMJGV5W%2FPbGxU%3D&id2=UU8Br6xLISU1Nw%3D%3D; t=0daad4d24c2e885afd9fa8716baa026e; miid=1048180764940120406; lgc=%5Cu6211%5Cu5BB6%5Cu5C0F%5Cu732A%5Cu54EA%5Cu6709%5Cu8FD9%5Cu4E48%5Cu53EF%5Cu7231; cna=Vj9nFHanAj8CAXOcj6YBcRmp; tracknick=%5Cu6211%5Cu5BB6%5Cu5C0F%5Cu732A%5Cu54EA%5Cu6709%5Cu8FD9%5Cu4E48%5Cu53EF%5Cu7231; l=cBMYtzcnQN77UlmaBOfClurza77TgI9T8kPzaNbMiICPOP5k5xZAWZmDo0TDCn1VK6PXB3ln6AW2B5TFayIq0-Y3LAaZk_f..; tg=0; uc1=cookie14=UoTblAO0EGmWkw%3D%3D; mt=ci=-1_0; cookie2=5b4660f6f6fb8a80d6be8cb60d9f157f; v=0; _tb_token_=eeeae3533e6b3',
            'Host': 's.taobao.com',
            'Referer': 'https://www.taobao.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'
        }
    url = ''

    with open('taobao.csv', 'w', encoding='utf-8', newline='') as f:        # 创建文件对象
        csv_writer = csv.writer(f)          # 基于文件对象构建 csv写入对象
        csv_writer.writerow( ["商品ID","宝贝名称","当前月付款人数","评论条数","评论页url"] )   # 构建列表头
        while i<=pageNum:
            if i>1:
                time.sleep( random.random()*10 )# 等待0~10秒随机时间，防止反爬
                headers['Referer'] = url        # 若是第二页、第三页等，则将来源页换为上一次的url，防止反爬
            # 几个重要字段：q=***是要查询的关键字；sort规定了按销量排序；s=int是从第几个商品开始（淘宝页面上，1页至多显示44个商品，第一页为s=0）
            url = 'https://s.taobao.com/search?q='+keyword+'&search_type=item&ie=utf8&sort=sale-desc&bcoffset=0&s='+str( (i-1)*44 )
            resp = sendGet(url, headers)
            soup = BeautifulSoup( resp.content.decode('UTF-8'), 'html.parser' )
            try:
                # 获取script中含有所需JSON信息的一项字符串
                script = soup.find("script", string=re.compile('g_page_config')).text.strip()
                jsons = parseBracket( script )[0]
                jsons = parseBracket( jsons, trigger="{", num=44 )
                #for each in jsons:
                #    print(each, "\n")
                # 首次访问时获取总页数
                if i==1:
                    pageLoc = script.find("pager")      # 定位到pager数据所在位置
                    pageData = parseBracket( script[pageLoc:], trigger="{", num=1 )[0]
                    pageNum = json.loads(pageData)["data"]["totalPage"]
                    print("\n>> 开始抓取该产品的淘宝商品信息，共"+str(pageNum)+"页。")
            except Exception as e:
                print(">> 当前页面没有宝贝！",e)
                saveToFile( resp.content.decode('UTF-8'), 'taobao_SK-II.txt' )
                break

            sys.stdout.write('\r>> 当前处理第'+str(i)+'页……')
            for json_str in jsons:
                try:
                    obj = json.loads(json_str)
                    ID = obj["nid"]
                    name = obj["raw_title"].replace(",", "，").strip()     # 将正文中所有的半角逗号改为全角逗号，避免存储为csv文件后混淆
                    # sales 这一项有的店铺没有给出。它是指付款人数（不等于月销量。通常月销量>付款人数）
                    sales = obj["view_sales"] if ("view_sales" in obj) else "-"
                    ccnt = obj["comment_count"]
                    link = obj["comment_url"]
                    csv_writer.writerow( [ID, name, sales, ccnt, link] )
                except Exception as e:
                    print("\n>> 页内检索过程出错：",e)
                    continue
        
            i += 1
    print("\n>> 抓取完成！")

if __name__ == "__main__":
    main()
