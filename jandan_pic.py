# coding=utf-8
from urllib.parse import urljoin, urlencode
import requests
import http.cookiejar
import socket
import os
from hashlib import md5
from base64 import b64encode, b64decode
import sys
import time
import re
from random import random
from bs4 import BeautifulSoup as BS
import pymysql
socket.setdefaulttimeout(10)

config = {
    'host':'127.0.0.1',
    'port':3306,
    'user':'root',
    'password':'123456',
    'db':'test',
    'charset':'utf8mb4',
    'cursorclass':pymysql.cursors.DictCursor,
}

session = requests.Session()
headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
'Connection': 'keep-alive',
'Host': 'jandan.net',
'Referer': 'https://jandan.net/',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3322.3 Safari/537.36'    
}

conn = pymysql.connect(**config)  #数据库连接设置
cursor = conn.cursor()

# 递归遍历
def start_request(url):
    r = session.get(url, headers=headers, timeout=10)
    soup = BS(r.text, 'html.parser')
    next_page = soup.find('a', class_='previous-comment-page')
    writeDb(soup)  #保存到数据库
    if next_page != None:
        start_request(urljoin(url, next_page.get('href')))

# 组装绝对路径
def destFile(url, store_dir):
    if not os.path.isdir(store_dir):
        os.mkdir(store_dir)
    pos = url.rindex('/')
    return os.path.join(store_dir, url[pos+1:])
          
# 解析页面, 获取图片地址, 下载到本地
def download(soup):
    spans = soup.find_all('span', class_='img-hash')
    for span in spans:
        img_hash = span.text
        href = b64decode(img_hash).decode('utf-8')
        if href.startswith('//'):
            href = "http:{0}".format(href)
        elif href.startswith('http'):
            pass
        try:
            file = destFile(href, store_dir)
            if os.path.exists(file):
                print('%s has been crawled' % file)
                continue
            urllib.request.urlretrieve(href, file)
            print(href)
        except Exception as e:
            print(e, href)
            urllib.request.urlretrieve(href, destFile(href, store_dir))

# 解析页面, 获取图片地址, 写入数据库
def writeDb(soup):
    texts = soup.find_all('div', class_='text')
    for text in texts:
        spans = text.find_all('span', class_='img-hash')
        id = text.find('span', class_='righttext').text
        if int(id) > last_id:
            for span in spans:
                img_hash = span.text
                href = b64decode(img_hash).decode('utf-8')
                if href.startswith('//'):
                    href = "https:{0}".format(href)
                elif href.startswith('http'):
                    pass
                large = href.replace('/mw600/', '/large/')
                print(id, large)
                try:
                    cursor.execute('insert into jandan(large, mw) values(%s, %s)', (large, href))
                    conn.commit()
                except Exception as e:
                    print(e)
        else:
            print('finished')
            sys.exit(0)

# 获取加密串
def getEncodeKey():
    r = session.get('https://jandan.net/ooxx', headers=headers, timeout=10)
    js_reg = re.findall(r'src="//cdn.jandan.net/static/min/[\w\d\.]+.js"', r.text)
    try:
        js_url = 'https:' + js_reg[len(js_reg) - 1][5:-1]
        r = session.get(js_url+'?rm='+str(random()), headers=headers, timeout=10)
        app_secret = re.findall(r'c=[\w\d]+\(e,\"[\w\d]+\"\);', r.text)
        app_secret = app_secret[0].split('"')[1]
        return app_secret
    except Exception as e:
        print("获取加密串失败")
        sys.exit(0)
        
# 关闭数据库指针、数据库连接
def close():
    if cursor:
        cursor.close()
    if conn:
        conn.close()
        
if __name__ == '__main__':
    store_dir = r'F:\ooxx'  #保存路径
    last_id = 3692992  #最后获取到的楼层id

    try:
        start_request('https://jandan.net/ooxx')
    except KeyboardInterrupt as e:
        print('quit')
    finally:
        close()
