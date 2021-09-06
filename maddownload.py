import jieba
import jieba.posseg as pseg
import random
import time
import urllib.request
import json
import os
from io import StringIO
from html.parser import HTMLParser

IPFS_GATEWAY = 'https://cf-ipfs.com/ipfs/'
MATATAKI_LIST_LINK = 'https://api.mttk.net/posts/timeRanking?author=2331'
MATATAKI_ARTICLE_LINK = 'https://www.matataki.io/p/'
MATATAKI_ARTICLE_IPFS_API = 'https://api.mttk.net/p/{0}/ipfs'
USE_IPFS_GATEWAY = False


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def screen_clear():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')


def getArticleList():
    articles = []
    print('\nFetching article list...')
    with urllib.request.urlopen(MATATAKI_LIST_LINK) as url:
        data = json.loads(url.read().decode())
        articles = data['data']['list']
    return articles


def getArticleText(article):
    articleId = article['id']
    articleHash = article['hash']
    screen_clear()
    print('\nFetching text for ' + articleHash + '...')
    if (USE_IPFS_GATEWAY):
        texturl = IPFS_GATEWAY + articleHash
    else:
        texturl = MATATAKI_ARTICLE_LINK+str(articleId)
    articleText = ''
    with urllib.request.urlopen(texturl) as response:
        html = response.read().decode('utf-8')
        articleText = strip_tags(html)
    return articleText


articles = getArticleList()


def getHtmlHash(articleId):
    htmlHash = ''
    articleIpfsApi = MATATAKI_ARTICLE_IPFS_API.format(articleId)
    with urllib.request.urlopen(articleIpfsApi) as url:
        data = json.loads(url.read().decode())
        htmlHash = data['data'][0]['htmlHash']
    return htmlHash


for article in articles:
    
    ipfsHash = getHtmlHash(article['id'])
    articleText = getArticleText(article)
    articleText = articleText.split('本文内容已上传星际文件存储系统「IPFS」，永久保存。')[1]
    articleText = articleText.split('免责声明：本文由用户')[0]
    print(articleText)
    filename = "downloaded\\"+ipfsHash+".txt"
    text_file = open(filename,mode='w',encoding='utf-8')
    n = text_file.write(articleText)
    text_file.close()
