from douban_crawler import DoubanTopCrawler
from mysql_helper import MySqlHelper

# 初始化爬虫
crawler = DoubanTopCrawler()
movies = crawler.fetch_top100()

# 初始化数据库连接
db = MySqlHelper(
    host='localhost',
    user='root',
    password='921269481',
    database='doubantop_db'
)

# 插入数据
for movie in movies:
    insert_sql = """
    INSERT INTO douban_top100 
        (`rank`, title, director, actors, score, year, region, cover, url)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    db.execute(insert_sql, (
        movie['rank'],
        movie['title'],
        movie['director'],
        movie['actors'],
        movie['score'],
        movie['year'],
        movie['region'],
        movie['cover'],
        movie['url'],
    ))


results = db.fetch_all("SELECT * FROM douban_top100 LIMIT 5;")# 查看前5条记录
for row in results:
    print(row)

db.close()