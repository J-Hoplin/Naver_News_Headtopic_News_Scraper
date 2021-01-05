Naver News Scraper : Topic by Topic
===
***

1 . 기능 : [네이버 뉴스](https://news.naver.com/)를 보시면 각 분야(ex : 정치, 경제, 그날의 헤드라인 등)의 대표 뉴스들이 있습니다. 그 시간대(이 크롤러를 실행하는 시점)의 대표 뉴스들의 제목, 링크, 기사 내용 텍스트를 가져와서 JSON으로 저장하는 크롤러입니다

2 . [코드](https://github.com/J-hoplin1/Naver_News_Headtopic_News_Scraper/blob/master/Naver_News_Scraper_Algorithm/Basic_Crawler.py)

3 . [예시 JSON](https://github.com/J-hoplin1/Naver_News_Headtopic_News_Scraper/blob/master/Naver_News_Scraper_Algorithm/NaverNewsHeadlineScrape_2020-06-21.json)
***
- 2020 / 12 / 14
  - Bug fix : http.client.RemoteDisconnected: Remote end closed connection without response 라는 메세지의 에러가 발생
  - Fix : Header에 User-Agent값을 넣어서 봇으로 인식하는것을 방지
  - TODO : asyncio 모듈을 활용하여 비동기적 scraping 처리

- 2021 / 01 / 05
  - Bug fix : [불필요한 script tag의 주석 text가 기사문에 함께 반환되는것을 방지](https://github.com/J-hoplin1/Naver_News_Headtopic_News_Scraper/blob/0454da61755f1f69e0b507a242fb41fe6cf1e1e9/Naver_News_Scraper_Algorithm/Basic_Crawler.py#L51)
