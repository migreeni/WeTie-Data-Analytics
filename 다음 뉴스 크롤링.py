import json
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
import csv

# 날짜리스트 만들기
base = datetime.strptime('20191126', '%Y%m%d')
numdays = 365
date_list = [(base + timedelta(days=x)).strftime('%Y%m%d') for x in range(0, numdays)]
print(len(date_list))

def onedate_url(date):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    url = "https://news.daum.net/breakingnews/culture?regDate={}"
    url_list = []
    for dt in date:
        i = 0
        while i<1: 
            i+=1
            res = requests.get(url.format(dt), headers=headers)
            if res.status_code == 200:
                html = bs(res.text, 'html.parser')
                cont = html.find('ul',{'class': 'list_news2 list_allnews'})
                try:
                    items = cont.findAll('li')
                except Exception as e:
                    print(str(e))
                    break
                else:
                    for item in items[0:10]:
                        tit = item.find('strong',{'class':'tit_thumb'}).a
                        url_list.append(tit['href'])
            else:
                print(res.status_code)

    return url_list

url_list = onedate_url(date_list)

# csv에 쓰기
f = open('daum_crawling.csv','w', newline = '', encoding='utf-8')
wr = csv.writer(f)
wr.writerow(['날짜','제목','내용'])
for k in range(len(url_list)):
    a = []
    res = requests.get(url_list[k])
    soup = bs(res.text, 'html.parser')

    figcaptions = soup.select('figcaption')

    for figcaption in figcaptions:
        figcaption.extract()

    title = soup.select_one('h3.tit_view')
    content = soup.select_one('div#harmonyContainer')

    if type(title) != type(None) and type(content) != type(None):

        a.append(date_list[k//10])
        a.append(title.text)
        a.append(content.text.strip())
        wr.writerow(a)


f.close()

