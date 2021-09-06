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
    with open('downloaded/list.json',encoding='utf-8') as fp:
        data = json.load(fp)
        articles = data['data']['list']
    return articles


def getArticleText(article):
    articleId = article['id']
    articleHash = article['hash']
    screen_clear()
    print('\nFetching text for ' + articleHash + '...')

    articleText = ''
    with open('downloaded/'+articleHash+'.txt',encoding='utf-8') as fp:
        html = fp.read()
        articleText = strip_tags(html)
    return articleText


articles = getArticleList()

while True:
    article = random.choice(articles)
    ipfsHash = article['hash']
    title = article['title']
    articleText = getArticleText(article)
    seg_list = pseg.cut(articleText)

    nounset = set()
    verbset = set()
    adjset = set()
    for word, flag in seg_list:
        #print(word, flag)
        if (flag == 'n'):
            nounset.add(word)
        if (flag == 'v'):
            verbset.add(word)
        if (flag == 'a'):
            adjset.add(word)

    nounlist = list(nounset)
    verblist = list(verbset)
    adjlist = list(adjset)

    screenText = ''
    screen_clear()

    iFrom = random.choice(['我从', '我在'])
    haveASee = random.choice([' 看了一眼', ' 读了一遍', ' 拜读了'])
    ifound = random.choice(['发现', '觉得', '知道了'])
    introTemplate = "{0} {1} {2}《{3}》{4}："

    print(introTemplate.format(iFrom, ipfsHash, haveASee, title, ifound))
    while(len(screenText) < 840):
        noun1 = random.choice(nounlist)
        verb1 = random.choice(verblist)
        adj1 = random.choice(adjlist)
        noun2 = random.choice(nounlist)

        shape = random.randint(1, 5)
        if (shape == 1):
            newText = noun1+verb1+'了'+adj1+'的'+noun2
        if (shape == 2):
            newText = noun1+verb1+adj1+noun2
        if (shape == 3):
            newText = noun1+verb1+'了'+adj1+noun2
        if (shape == 4):
            newText = noun1+verb1+adj1+'的'+noun2
        if (shape == 5):
            newText = noun1+verb1+noun2

        seperators = ['', '，', '，', '，', '。', '。', '；', '。\n']
        seperator = random.choice(seperators)
        print(newText, end=seperator, flush=True)
        screenText = screenText + newText
        screenText = screenText + seperator

        waitTime = round(random.uniform(0.4, 1.0), 10)
        time.sleep(waitTime)
