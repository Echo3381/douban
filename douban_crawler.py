import requests
from bs4 import BeautifulSoup
import time
import random

class DoubanTopCrawler:
    def __init__(self):
        self.base_url = "https://movie.douban.com/top250"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

    def fetch_html(self, start):
        params = {'start': start}
        response = requests.get(self.base_url, headers=self.headers, params=params)
        response.encoding = 'utf-8'
        return response.text

    def parse_html(self, html, rank_offset):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.select('div.item')
        result = []

        for i, item in enumerate(items):
            rank = rank_offset + i + 1 #排名
            title = item.select_one('.title').get_text(strip=True) #电影名
            score = float(item.select_one('.rating_num').get_text(strip=True)) #评分
            cover = item.select_one('img').get('src') #图片地址
            url = item.select_one('a').get('href') #详细地址

            director = None #导演
            actors = None #主演
            year = None #年份
            region = None #地区

            try:
                info_text = item.select_one('.bd p').get_text().strip()
                lines = info_text.split('\n')#分为两行
                if len(lines) >= 2:
                    line1 = lines[0].strip().replace('\xa0', '')#去除非断行空格，不处理可能会导致分割失败
                    if '导演' in line1:
                        director_part = line1.split('主演')[0].replace('导演:', '').strip()#按照“主演”分割，保留前半部分，并去除“导演”文字
                        director = director_part
                    if '主演' in line1:
                        actor_part = line1.split('主演:')[-1].strip()#按“主演:”分割字符串，取后面部分
                        actors = actor_part

                    line2 = lines[1].split('/')
                    if len(line2) >= 2:
                        year_str = line2[0].strip()
                        year = int(year_str) if year_str.isdigit() else None
                        region = line2[1].strip()
            except Exception as e:
                print("解析失败:", e)

            result.append({
                'rank': rank,
                'title': title,
                'director': director,
                'actors': actors,
                'score': score,
                'year': year,
                'region': region,
                'cover': cover,
                'url': url
            })

        return result

    def fetch_top100(self):
        all_movies = []
        for page in range(4):
            start = page * 25
            html = self.fetch_html(start)
            page_movies = self.parse_html(html, start) #爬虫
            all_movies.extend(page_movies) #把当前页的结果加入总列表
            time.sleep(random.uniform(1, 2.5)) #延时随机秒数，防止封ip
        return all_movies
