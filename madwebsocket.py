import sys
import jieba.posseg as pseg
import random

import glob
import os
import re
import asyncio
import websockets

def strip_tags(textWithLink):
    cleanText = re.sub(r'\[http.*?\]', '', textWithLink)
    lines = cleanText.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]
    cleanText = "\n".join(non_empty_lines)
    return cleanText


def screen_clear():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')


def getArticleList():
    articles = []
    path = "offline_data/*.txt"
    for filename in glob.glob(path):
        with open(filename, 'r', encoding="utf-8") as file:
            head = [next(file) for x in range(7)]
        articles.append({"filename": filename, "title": head[0].strip()})

    return articles


def getArticleText(article):
    filename = article['filename']
    screen_clear()

    articleText = ''
    with open(filename, encoding='utf-8') as fp:
        fileLines = fp.readlines()[7:]
        html = "".join(fileLines)
        articleText = strip_tags(html)
    return articleText


articles = getArticleList()
async def writeToSocket(websocket):
    while True:
        article = random.choice(articles)
        articleText = getArticleText(article)
        seg_list = pseg.cut(articleText)
        nounset = set()
        verbset = set()
        adjset = set()
        for word, flag in seg_list:
            
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
        introTemplate = "\r\n{0} {1} {2}《{3}》{4}：\r\n"

        greeting = introTemplate.format(iFrom, "古董电脑室", haveASee, article['title'], ifound)

        await websocket.send(bytearray(greeting,encoding='gbk'))

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

            seperators = ['', '，', '，', '，', '。', '。', '；', '。\r\n']
            seperator = random.choice(seperators)
            newText += seperator
            
            await websocket.send(bytearray(newText,encoding='gbk'))

            screenText = screenText + newText
            screenText = screenText + seperator

            waitTime = round(random.uniform(0.4, 1.0), 10)
            await asyncio.sleep(waitTime)

async def echo(websocket):
    async for message in websocket:
        await websocket.send(message)

async def main():
    async with websockets.serve(writeToSocket, "", 8082, subprotocols=["binary"]):
        await asyncio.Future()  # run forever

asyncio.run(main())
