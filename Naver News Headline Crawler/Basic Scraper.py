# This code is written by Hoplin
# Code last edited : 2020/06/20
# Description : This code will be used as algorithm of 'The Camp' News Sending program  

import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import URLError
from urllib.request import HTTPError
import sys
import time
import re

# Save News Datas : Data include articles, title
newsDatas = dict()
# News Topics will be save here
newsTopics = []

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
    sectionElements = sectionElements[:-1]
    for topic in sectionElements:
        capsule = dict()
        topicName = topic.find('h4').text
        articlesInformation = topic.findAll('li')
        for inf in range(len(articlesInformation)):
            capsule['article' + '_' +str(inf)] = [articlesInformation[inf].find('a')['href'],articlesInformation[inf].find('a').text.strip()]
        newsDatas[topicName] = capsule
        
    
    print(newsDatas)
except URLError as errormessageURL:
    print(errormessageURL)

except HTTPError as errormessageHTTP:
    print(errormessageHTTP)
