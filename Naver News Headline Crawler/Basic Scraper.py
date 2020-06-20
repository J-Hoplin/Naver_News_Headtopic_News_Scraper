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

    '''
    Example result

    {'헤드라인 뉴스beta': {'article_0': ['/main/read.nhn?mode=LSD&mid=shm&sid1=100&oid=052&aid=0001455083', '절로 들어간 주호영..."상황 바뀐 것 없다"[단독 인터뷰]'], 'article_1': ['/main
/read.nhn?mode=LSD&mid=shm&sid1=104&oid=081&aid=0003100694', '“홍콩 분열세력 감시·처벌” 중국, ‘홍콩 국가안보처’ 신설한다'], 'article_2': ['/main/read.nhn?mode=LSD&mid=shm&sid1=100&oi
d=052&aid=0001455062', '방미 이도훈 귀국..."항상 소통하고 있다"'], 'article_3': ['/main/read.nhn?mode=LSD&mid=shm&sid1=102&oid=055&aid=0000822719', "참사 53일 만에…이천 화재 참사 '눈
물의 영결식'"], 'article_4': ['/main/read.nhn?mode=LSD&mid=shm&sid1=102&oid=421&aid=0004707618', '\'마스크 실랑이\' 첫 구속…"승객 안전·건강 직결 사안"(종합)']}, '정치': {'article_0':
 ['https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=100&oid=081&aid=0003100693', '南 보란 듯 北, 북중정상회담 1주년 “각별”…시진핑 방북 대상영'], 'article_1': ['https://news
.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=100&oid=277&aid=0004702499', '[종합]\'文 대통령 얼굴에 담뱃재\' 北, 대남 전단 준비…"최고 존엄 건드려"…탈북단체도 삐라 살포 준비'], 'art
icle_2': ['https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=100&oid=052&aid=0001455063', '볼턴 "북미회담 방해하려 했다"...\'탑 다운\' 한계 확인?'], 'article_3': ['https://n
ews.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=100&oid=001&aid=0011692089', '북, 북중정상회담 1주년 우호과시…회담 영상도 방송(종합)'], 'article_4': ['https://news.naver.com/main/r
ead.nhn?mode=LSD&mid=shm&sid1=100&oid=025&aid=0003010778', '고민정 "요 며칠 많이 지쳐 있었다···나는 누구인가 되뇌어"']}, '경제': {'article_0': ['https://news.naver.com/main/read.nhn?
mode=LSD&mid=shm&sid1=101&oid=055&aid=0000822720', "다음 달부터 '재포장 묶음 할인' 금지…소비자 혼란"], 'article_1': ['https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=101&o
id=448&aid=0000300394', '[따져보니] 묶음할인 안된다?…재포장금지법 논란'], 'article_2': ['https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=101&oid=052&aid=0001455031', '복잡
해진 전세대출 규정..."나는 대출받을 수 있을까?"'], 'article_3': ['https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=101&oid=277&aid=0004702468', '복잡한 \'부동산 대책\'에 실
수요자들 혼란…"분양권 대출 어떡해"'], 'article_4': ['https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=101&oid=014&aid=0004446729', '日 "경기 하강 멈추는 중"...경기판단 상향
 조정']}, '사회': {'article_0': ['https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=102&oid=052&aid=0001455086', "'검·언 유착' 의혹, 외부 전문가 판단 받는다...대검, 진정 수
용"], 'article_1': ['https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=102&oid=052&aid=0001455082', '"질 낮은 수업과 시험"에도...대학은 \'등록금 반환\' 외면'], 'article_2':
['https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=102&oid=052&aid=0001455080', '임신부 탄 승용차 옹벽 사이로 추락...무사히 구조돼'], 'article_3': ['https://news.naver.com/
main/read.nhn?mode=LSD&mid=shm&sid1=102&oid=052&aid=0001455077', '대전 산업단지 공장 큰불...헬기 투입 진화'], 'article_4': ['https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid
1=102&oid=052&aid=0001455075', "잘못된 호적 바꾸려다 '무국적' 위기...어떻게 된 걸까?"]}, '생활/문화': {'article_0': ['https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=103&o
id=055&aid=0000822726', "'수궁가' 맞춰 댄스 · 떼창…고정관념 깬 팝 밴드"], 'article_1': ['https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=103&oid=055&aid=0000822725', "뿌리
 깊은 '핵 철폐=망하는 길'…다큐로 본 북한의 속내"], 'article_2': ['https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=103&oid=031&aid=0000543787', '[인터뷰] 바이올리니스트 임
지영 “바흐·이자이 무반주곡으로 음악 힘 전달”'], 'article_3': ['https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=103&oid=047&aid=0002273944', '살구며 앵두며 아무 때나 맘껏
따먹으라는 정원 주인'], 'article_4': ['https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=103&oid=584&aid=0000009236', '연어는 왜 中 베이징 코로나19 확산 주범으로 찍혔나']},
'세계': {'article_0': ['https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=104&oid=081&aid=0003100694', '“홍콩 분열세력 감시·처벌” 중국, ‘홍콩 국가안보처’ 신설한다'], 'articl
e_1': ['https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=104&oid=003&aid=0009925354', "'중국 잠수함', 일본 규슈 남부 접속수역 사흘간 침입 잠항"], 'article_2': ['https://new
s.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=104&oid=052&aid=0001455076', "美 노예해방 기념일 전국에 집회...트럼프 유세장 '충돌' 우려"], 'article_3': ['https://news.naver.com/main
/read.nhn?mode=LSD&mid=shm&sid1=104&oid=003&aid=0009925349', "中정부, 분열세력 감시 '홍콩 국가안보처' 신설키로(종합)"], 'article_4': ['https://news.naver.com/main/read.nhn?mode=LSD&m
id=shm&sid1=104&oid=003&aid=0009925345', '폼페이오 “홍콩을 중국 일부로 간주해 취급하겠다”경고']}, 'IT/과학': {'article_0': ['https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid
1=105&oid=293&aid=0000028954', "싸이월드를 대신한 요즘 서비스...다시 뜨는 '아바타'"], 'article_1': ['https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=105&oid=366&aid=000054
2707', '"면역 회피하는 코로나19…백신 나와도 효과 단기간"'], 'article_2': ['https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=105&oid=293&aid=0000028953', "'커뮤니티' 노리는
스타트업들"], 'article_3': ['https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=105&oid=011&aid=0003756439', "['약'한뉴스]중외제약이 아니라 'JW중외제약' 이에요"], 'article_4'
: ['https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=105&oid=081&aid=0003100670', '“코로나, -4℃에서 20년, -20℃에서도 수개월 생존” (中전문가)']}}
    '''
