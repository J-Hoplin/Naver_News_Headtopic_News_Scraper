# This code is written by Hoplin
# Code last edited : 2020/06/21
# Description : This code will be used as algorithm of 'The Camp' News Sending program  

import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import URLError
from urllib.request import HTTPError
import sys
import time
import re
import json
import time

# Save News Datas : Data include articles, title
newsDatas = dict()
# News Topics will be save here
newsTopics = []

def getArticleMainText(URL):
    html = urlopen(URL)
    html = BeautifulSoup(html,'html.parser')
    # 본문 내용은 id가 articleBodyContents 인 <div> 태그 안에있다.
    paragraphElements = re.sub(' +', ' ', html.find('div',{'id' : 'articleBodyContents'}).text).strip() # ' +' : white space가 한개 이상인 패턴을 찾는다.
    return paragraphElements
    
def JSONConverter(dataCapsule):
    with open('NaverNewsHeadlineScrape_' + str(time.strftime('%Y-%m-%d', time.localtime(time.time()))) + '.json','w',encoding="utf-8") as make_file:
        json.dump(dataCapsule,make_file,ensure_ascii=False,indent="\t") # indent : 들여쓰기값 Indent Parameter

try:
    naverNewsURL = 'https://news.naver.com/'
    html = urlopen(naverNewsURL)
    html = BeautifulSoup(html,'html.parser')
    
    
    '''
    Get elements : About each news section. There are 7 sections. 
    
    1. Today headline news 
    
    2. Economy
    
    3. Society
    
    4. Life
    
    5. World
    
    6. IT
    
    7. Politics
    '''
    sectionElements = html.find('div',{'class' : 'main_content_inner _content_inner'}).findAll('div',{'class' : re.compile('main\_component[A-Za-z]*')})
    del sectionElements[-1] # 맨 마지막에 필요 없는 데이터를 제거한다.
    
    # Last Scraped Time.
    newsDatas['lastScrapedTime'] = time.strftime('%c', time.localtime(time.time())) 
    # Source
    newsDatas['DataSource'] = 'Naver News'
    
    for topic in sectionElements:
        capsule = dict()
        topicName = topic.find('h4').text
        articlesInformation = topic.findAll('li')
        for inf in range(len(articlesInformation)):
            articleURL = articlesInformation[inf].find('a')['href']
            articleURLPatternChecker = re.compile('\/main\/[A-Za-z0-9]*')
            checkerBoolean = articleURLPatternChecker.match(articleURL)
            
            # Variable : article Text 
            articText = None
            if checkerBoolean:
                articText = getArticleMainText('https://news.naver.com' + articleURL)
            else:
                articText = getArticleMainText(articleURL)
            capsule['article' + '_' +str(inf + 1)] = {
                'articleTitle' : articlesInformation[inf].find('a').text.strip(),
                'url' : articleURL,
                'articleText' : articText
            }
                
        newsDatas[topicName] = capsule
    
    JSONConverter(newsDatas)

except URLError as errormessageURL:
    print(errormessageURL)
except HTTPError as errormessageHTTP:
    print(errormessageHTTP)
