import jieba
import jieba.posseg as pseg
import random
import time
import urllib.request
import json
import os
from io import StringIO
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
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

def getArticleIds():
    matatakiLink = 'https://api.mttk.net/posts/timeRanking?author=2331'
    articleIds = []
    with urllib.request.urlopen(matatakiLink) as url:
        data = json.loads(url.read().decode())
        articles = data['data']['list']
        for article in articles:
            articleIds.append(article['id'])
    return articleIds

def getArticleText(atricleId):
    texturl = 'https://www.matataki.io/p/'+str(atricleId)
    articleText = ''
    with urllib.request.urlopen(texturl) as response:
        html = response.read().decode('utf-8')
        articleText = strip_tags(html)
    return articleText

articleIds = getArticleIds()

while True:
    atricleId = random.choice(articleIds)
    articleText = getArticleText(atricleId)
    seg_list = pseg.cut(articleText)

    nounset = set()
    verbset = set()
    adjset = set()
    for word, flag in seg_list:
        #print(word, flag)
        if (flag == "n"):
            nounset.add(word)
        if (flag == "v"):
            verbset.add(word)
        if  (flag == "a"):
            adjset.add(word)

    nounlist = list(nounset)
    verblist = list(verbset)
    adjlist = list(adjset)

    screenText = ""
    screen_clear()
    while(len(screenText)<840):
        noun1 = random.choice(nounlist)
        verb1 = random.choice(verblist)
        adj1 = random.choice(adjlist)
        noun2 = random.choice(nounlist)

        shape = random.randint(1,5)
        if (shape == 1):
            newText = noun1+verb1+"了"+adj1+"的"+noun2
        if (shape == 2):
            newText = noun1+verb1+adj1+noun2
        if (shape == 3):
            newText = noun1+verb1+"了"+adj1+noun2
        if (shape == 4):
            newText = noun1+verb1+adj1+"的"+noun2
        if (shape == 5):
            newText = noun1+verb1+noun2

        seperators = ['','，','，','，','。','。','；','。\n']
        seperator = random.choice(seperators)
        print(newText, end = seperator,flush=True)
        screenText = screenText + newText
        screenText = screenText + seperator

        waitTime = round(random.uniform(0.4, 1.0), 10)
        time.sleep(waitTime)
