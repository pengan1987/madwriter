# Json To Text Converter
#This is a utility to convert JSON files provides by Zhihu API to raw text file, 
# the generated text file is suitable to use in madoffline.py, it also provided a 
# csv index for reuse these files for other purpose like Gopher/RSS servers.

from datetime import datetime
from html.parser import HTMLParser
from io import StringIO
import json
from urllib.parse import unquote

allTags = []

class MLStripper(HTMLParser):

    lastLink = ''

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_starttag(self, tag, attrs):
        if (tag == 'img'):
            self.text.write('(Image: ')
            for attr in attrs:
                if attr[0] == 'src':
                    self.text.write(attr[1]+')\n')
        if (tag == 'a'):
            for attr in attrs:
                if (attr[0]) == 'href':
                    self.lastLink = self.decode_zhihu(attr[1])
        if (tag == 'table'):
            self.text.write('\n')

    def handle_endtag(self, tag):
        if (['p', 'h1', 'h2', 'h3', 'table'].count(tag) > 0):
            self.text.write('\n\n')
        if (['br', 'tr'].count(tag) > 0):
            self.text.write('\n')
        if (['td', 'th'].count(tag) > 0):
            self.text.write('\t')
        if (tag == 'a' and self.lastLink.strip()):
            self.text.write(' (Link: '+self.lastLink.strip()+') ')
            self.lastLink = ''

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()

    def decode_zhihu(self, linkstr: str):
        if (linkstr.startswith('https://link.zhihu.com/?target=')):
            linkstr = linkstr.replace('https://link.zhihu.com/?target=', '')
            linkstr = unquote(linkstr)
        elif (linkstr.startswith('http://link.zhihu.com/?target=')):
            linkstr = linkstr.replace('http://link.zhihu.com/?target=', '')
            linkstr = unquote(linkstr)
        return linkstr

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

jsonSources = ['items100.json','items200.json','items300.json']
data = []
# These json file is fetched from Zhihu use APIv4 like
# https://www.zhihu.com/api/v4/columns/retrocomputing/items?limit=10&offset=20
for jsonSource in jsonSources:
    with open(jsonSource, encoding='utf-8') as fp:
        parsedJson = json.load(fp)
        data += parsedJson['data']

fileIndex = []

for article in data:
    title = article['title']
    created = article['created']
    pageId = article['id']
    content = article['content']
    author = article['author']
    cleanText = strip_tags(content)
    createtime = datetime.fromtimestamp(article['created'])
    modifiedtime = datetime.fromtimestamp(article['updated'])

    fileIndex.append(str(pageId) + ','+title+','+str(createtime)+'\n')

    filehead = []
    filehead.append(title+'\n\n')

    filehead.append('作者：'+author['name']+'\n')
    filehead.append('编号：'+str(pageId)+'\n')
    filehead.append('创建于：'+str(createtime)+'\n')
    filehead.append('修改于：'+str(modifiedtime)+'\n')
    filehead.append('--------------------'+'\n\n')

    target = 'offline_data\\'+str(pageId)+'.txt'
    with open(target, "w", encoding="gbk", errors='ignore') as dst:
        dst.writelines(filehead)
        dst.write(cleanText)
with open('offline_data\\index.csv', "w", encoding="gbk", errors='ignore') as dst:
    dst.writelines(fileIndex)
