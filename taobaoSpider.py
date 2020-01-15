import requests
import bs4
import re
import json
from bs4 import BeautifulSoup
from weiboSpider import saveToFile

def sendGet(keywords, page):
    headers={    
        'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.7, ja; q=0.3',
        'Cache-Control': 'max-age=0',
        'Cookie': 'cookie2=19785c0fc026d3fcc35542a60d0ddd09; _tb_token_=eefb566eb3ff6; v=0; uc1=cookie16=URm48syIJ1yk0MX2J7mAAEhTuw%3D%3D&cookie21=U%2BGCWk%2F7p4mBoUyS4E9C&cookie15=UtASsssmOIJ0bQ%3D%3D&existShop=false&pas=0&cookie14=UoTbldSgu40F2Q%3D%3D&tag=8&lng=zh_CN; csg=82b66cb2; dnk=%5Cu6211%5Cu5BB6%5Cu5C0F%5Cu732A%5Cu54EA%5Cu6709%5Cu8FD9%5Cu4E48%5Cu53EF%5Cu7231; skt=38fe6e426cf55355; existShop=MTU3ODY0OTc0MA%3D%3D; enc=Ua5usRIyWoZGZPq%2F24sc3QDLNNNg10CAxzfwjMrNNwRDIEP77I%2F3PxnMOtaAXblPBGoVx92Mri138Y9s00e91Q%3D%3D; uc4=id4=0%40U22GVfBGFOM6l7ocHkmNAOgBD2ga&nk4=0%40r7q0tQvWOx4NB3n0E47%2BxjwEgRCnh44keMuqxZXWeA%3D%3D; _cc_=URm48syIZQ%3D%3D; isg=BMTEt_QcRq89EvLsuiWCn56jjEK23ehH2AaFCt5hpw92CWHTBO9K15DjSWF0CiCf; thw=cn; uc3=nk2=rUsy40agieA1CAZiZZatPafMds0%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D&vt3=F8dBxdkMJGV5W%2FPbGxU%3D&id2=UU8Br6xLISU1Nw%3D%3D; t=0daad4d24c2e885afd9fa8716baa026e; miid=1048180764940120406; mt=ci=17_1; lgc=%5Cu6211%5Cu5BB6%5Cu5C0F%5Cu732A%5Cu54EA%5Cu6709%5Cu8FD9%5Cu4E48%5Cu53EF%5Cu7231; cna=Vj9nFHanAj8CAXOcj6YBcRmp; tracknick=%5Cu6211%5Cu5BB6%5Cu5C0F%5Cu732A%5Cu54EA%5Cu6709%5Cu8FD9%5Cu4E48%5Cu53EF%5Cu7231; l=dBMYtzcnQN77UHEXBOfZ-urza77tWCJOCkPzaNbMiICP9B16fn4hWZDT-k8BCn1VHstv-3ln6AW2BXTO9yCZJxpsw3k_J_4Z3dC..; tg=0; hng=CN%7Czh-CN%7CCNY%7C156; JSESSIONID=5E3C92040953761CF4500FC2C089366A',
        'Host': 's.taobao.com',
        'Referer': 'https://s.taobao.com/search',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'
    }
    payload = {'q':keywords, 'sort':"sale-desc", 's':(page-1)*44}  # q=***是要查询的关键字；sort规定了按销量排序；s=int是从第几个商品开始（淘宝页面上，1页至多显示44个商品，第一页为s=0）
    url = "https://s.taobao.com/search"
    try:
        res = requests.get(url, headers=headers, params = payload)  # params用于get请求；data用于post请求。
    except Exception as e:
        print(e)
        return None
    return res

def get_item(res):
    g_page_config = re.search(r'g_page_config = (.*?);\n', res.text)
    page_config_json = json.loads(g_page_config.group(1))
    page_item = page_config_json['mods']['itemlist']['data']['auctions']
    result = []       # 整理出我们关注的信息(ID,标题，链接，售价，销量和商家)
    for each in page_item:
        dict1 = dict.fromkeys(('id','title','link','price','sale','shoper'))
        dict1['id'] = each['nid']
        dict1['title'] = each['title']
        dict1['link'] = each['detail_url']
        dict1['price'] = each['view_price']
        dict1['sale'] = each['view_sales']
        dict1['shoper'] = each['nick']
        result.append(dict1)
        return result

def count_sales(items):
    count = 0 
    for each in items:
        if '###' in each['title']: #规定只取标题中‘###’的商品
            count += int(re.search(r'\d+',each['sale']).group())
            return count

def main():
    keywords = input("请输入搜索关键词：")  # 可以为各种商品名称
    resp = sendGet(keywords, 0)
    soup = BeautifulSoup( resp.content.decode('UTF-8'), 'html.parser' )
    print(soup)
    saveToFile( resp.content.decode('UTF-8'), 'taobao_SK-II.txt' )
    '''length = 10    #淘宝商品页数
    total = 0
    for each in range(length):
        res = open(keywords, each+1)
        items = get_item(res)
        total += count_sales(items)       #销售总量
        print(total)'''

if __name__ == "__main__":
    main()
