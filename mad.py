"""
Mad Writer
by Pengan Zhou
Tested with Python 3.7 on Windows 10 and Debian 10
April 23, 2021
This software is release in NFT License 2.0
https://www.nftlicense.org/

This script generate randomized articles from my writing works on Matataki.io
The writing works on Matataki.io is also stored in IPFS
So even you don't have access to Matataki, you can find my works on IPFS

Here is some IPFS hashes for my work:

QmanyZNAsoFDJDhhzPbT9UFWsg7SckoqKpVQuRx9UnroSQ
QmbjDot829jihsVq7MJmEXeCQFm77A6YqzjDTKA5sPFaBK
QmcuJ3Fsim7qpCgZC3n54Z9cQqgK9iPE73f83x1UQP6vkp
QmNWTa94ZqUQGCUgikHGTt4TbvJZYNpmxjAYnzYvSjLmZr
QmNyuEte4me9Xb9yAf2bpVEUdEAzSy99rZ4S1MgW5azbdx
QmP4hN87r2KNAVn3r87NqvNF7sqfU7EYztPSUdCo9DTQN6
QmPCwHAKZKLoEeJFwwweBWmwW8mSTw8Uw7ykDqDACQunGq
QmPSs26TuUTGzaqG3qgU7WPKdFXxXDH9aPmHFRFAtB5Syt
QmSS4MhbVTBpX9XLz3UXmApW5knpTqHyc23sZkBpEJgpqN
QmTwgTyDoxm8JaacweCWe98b1JgtKrWrNY4Lg8xDodzmZT
QmU8t21vtmw4rxjd3ByvitQc744Q2ErKM8m35PSp3weZwE
QmUnFyW8XKtjJftaooDTAB4NEAhMRndVzADeFYAFoKX96E
QmUnyfkapQSXdJwZJxEw5x56yDDxUWy6WGwWPLzDyLEvve
QmWA3RsQTvZnGae7qUBXEt6PRRw9HCD6HQ93Q1YqNVEBXM
QmWxLrK3tkgKKsrKmToZ9RHadNE88Sh8LVoXNw4v9LwJLb
QmXreavjHDLzsojQYz6exQ4e2ub3D61KBZiudsQQDjQx8b
QmYPYENCv2DwJLmFY2sTii6FG5Kv3RBuqibJBZnxnyhmFj
QmZKphhjCBkWU3pkYqFwnna31xzuS8SokBSeNyUYL9nnGV
QmZL56iY9yk5fSzMEJTo3jJUjH89aXkye1y9Vu66cG97Fn
QmZukHACQnFxwPocm9Zwv1RQ5Vd42mARbiH1aWW8HHWJUS
"""

import jieba
import jieba.posseg as pseg
import random
import time
import urllib.request
import json
import os
from io import StringIO
from html.parser import HTMLParser

IPFS_GATEWAY = 'https://ipfs.eth.aragon.network/ipfs/'
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
    apiArticles = []
    print('\nFetching article list...')
    with urllib.request.urlopen(MATATAKI_LIST_LINK) as url:
        data = json.loads(url.read().decode())
        apiArticles = data['data']['list']
    return apiArticles


def getHtmlHash(articleId):
    htmlHash = ''
    articleIpfsApi = MATATAKI_ARTICLE_IPFS_API.format(articleId)
    with urllib.request.urlopen(articleIpfsApi) as url:
        data = json.loads(url.read().decode())
        htmlHash = data['data'][0]['htmlHash']
    return htmlHash


def getArticleText(article):
    articleId = article['id']
    htmlHash = article['htmlHash']

    screen_clear()
    print('\nFetching text for ' + str(articleId) + ': '+htmlHash+'...')

    htmlHash = article['htmlHash']
    if (USE_IPFS_GATEWAY):
        texturl = IPFS_GATEWAY + htmlHash
        print("Using IPFS gateway:\n"+texturl)
    else:
        texturl = MATATAKI_ARTICLE_LINK+str(articleId)
        print("Using Matataki website:\n"+texturl)
    articleText = ''
    with urllib.request.urlopen(texturl) as response:
        html = response.read().decode('utf-8')
        articleText = strip_tags(html)
    return articleText


articles = getArticleList()

while True:
    article = random.choice(articles)
    htmlHash = getHtmlHash(article['id'])
    article['htmlHash'] = htmlHash
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

    print(introTemplate.format(iFrom, htmlHash, haveASee, title, ifound))
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
