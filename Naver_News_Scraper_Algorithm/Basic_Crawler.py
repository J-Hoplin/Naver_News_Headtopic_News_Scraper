# This code is written by Hoplin
# Code last edited : 2020/06/20
# Description : This code will be used as algorithm of 'The Camp' News Sending program  

import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import URLError
from urllib.request import HTTPError
import requests
import sys
import time
import re
import json
import time
import asyncio

# Save News Datas : Data include articles, title
newsDatas = dict()
# News Topics will be save here
newsTopics = []

def returnHyperTextAddingHeader(URL):
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    html = session.get(URL,headers=headers).content 
    html = BeautifulSoup(html,"html.parser")
    return html

#각 섹션별 기사URL에 대해 기사 출력
def getArticleMainText(URL):
    '''
    html = urlopen(URL)
    html = BeautifulSoup(html,'html.parser')
    
    왜 이부분을 주석처리하고 사용하지 않나요?
    이 전에 다음과 같은 오류가 발생했었습니다.
    http.client.RemoteDisconnected: Remote end closed connection without response
    이러한 오류가 발생하는 이유는 요청을 받는 서버에서 요청을 비정상적이 요청으로 인지하고
    차단하는 경우에 발생하게 된다. 물론 서버 마다 다르지만 이렇게 차단된 상태의 html을 출력해 보면
    '비정상적인 요청에 따른 일시적 제한' 등의 글이 써져있는것을 볼 수 있다.
    결론적으로 말하면 뷰봇과 같은 '봇'으로 인식을 한 것이다.
    이렇게 봇으로 인식하는것을 방지하기 위해서는 패킷 header 정보에 User-Agent 정보를 넣어주면된다.
    '''

    html = returnHyperTextAddingHeader(URL)
    # 본문 내용은 id가 articleBodyContents 인 <div> 태그 안에있다.
    paragraphElements = re.sub('<script.*?>.*?</script>','',str(html.find('div',{'id' : 'articleBodyContents'})),0,re.I|re.S) # 0 : 부합되는 모든 문자열을 지우라는 의미,1을적으면 <script>만 지워지게됨 re.I (케이스 무시), re.S (점이 모든 문자와 일치) https://python.flowdas.com/library/re.html
    paragraphElements = re.sub(' +', ' ',BeautifulSoup(paragraphElements,"html.parser").text).strip() # ' +' : white space가 한개 이상인 패턴을 찾는다. 불필요한 <script>를 없애기 위해 string으로 되었던것을 다시 bs4.element.tag type으로 변경해준다.
    return paragraphElements
    
def JSONConverter(dataCapsule):
    with open('NaverNewsHeadlineScrape_' + str(time.strftime('%Y-%m-%d', time.localtime(time.time()))) + '.json','w',encoding="utf-8") as make_file:
        json.dump(dataCapsule,make_file,ensure_ascii=False,indent="\t") # indent : 들여쓰기값 Indent Parameter

try:
    naverNewsURL = 'https://news.naver.com/'
    html = returnHyperTextAddingHeader(naverNewsURL)
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
            
            # Article Text Scrape Here
            
            # Headline News's URL Type : Full URL 
            # Other sections' News's URL Type : /main/~~~ 
            articText = None
            if checkerBoolean:
                articText = getArticleMainText('https://news.naver.com' + articleURL)
            else:
                articText = getArticleMainText(articleURL)
            capsule['article' + '_' +str(inf + 1)] = {
                'articleTitle' : articlesInformation[inf].find('a').text.strip().replace("\"","'"),
                'url' : articleURL,
                'articleText' : articText.replace("\t","").replace("\n","").replace("\"","'")
            }
                
        newsDatas[topicName] = capsule
    
    JSONConverter(newsDatas)
except URLError as errormessageURL:
    print(errormessageURL)
except HTTPError as errormessageHTTP:
    print(errormessageHTTP)
