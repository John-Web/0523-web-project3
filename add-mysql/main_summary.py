import pymysql
import json

db = pymysql.connect("localhost", "root", "11112222", "new_films", charset='utf8')
cursor = db.cursor()
cursor.execute("drop table if exists main")
cursor.execute("drop table if exists summary")

main_create = """CREATE TABLE main (
    _id char(15) primary key,
    ratingAverage char(5),
    ratingPeople char(10),
    star5 char(5), star4 char(5), star3 char(5), star2 char(5), star1 char(5), 
    title char(200),
    poster char(100),
    imdb char(15),
    year char(5),
    duration char(80)
)"""
summary_create = """CREATE TABLE summary (
    _id char(15) primary key,
    article text(2000)
)"""

cursor.execute(main_create)
# cursor.execute(summary_create)

main_text = []
summary_text = []
main_re = "insert into main(" \
          "_id, ratingAverage, ratingPeople, star5, star4, star3, star2, star1," \
          " title, poster, imdb, year, duration) values " \
          "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
summary_re = "insert into summary(_id, article) values (%s, %s)"

f = open('films_all.json', encoding='utf-8')
try:
    for i in range(0, 10000):
        if i % 100 == 0:
            print(u'正在载入第%s行......' % i)
        lines = f.readline()  # 使用逐行读取的方法
        j = json.loads(lines)  # 解析每一行数据

        if len(j['rating']['stars']):
            main_text.append((
                j['_id'], j['rating']['average'], j['rating']['rating_people'],
                j['rating']['stars'][0], j['rating']['stars'][1], j['rating']['stars'][2],
                j['rating']['stars'][3], j['rating']['stars'][4],
                j['title'], j['poster'], j['imdb'], j['year'], j['duration']
            ))
        else:
            main_text.append((
                j['_id'], j['rating']['average'], j['rating']['rating_people'],
                '0.0', '0.0', '0.0', '0.0', '0.0',
                j['title'], j['poster'], j['imdb'], j['year'], j['duration']
            ))
        # summary_text.append((j['_id'], j['summary']))

    cursor.executemany(main_re, main_text)
    db.commit()
    print("main success!")
    '''
    cursor.executemany(summary_re, summary_text)
    db.commit()
    print('summary success!')
    '''
except Exception as e:
    db.rollback()
    print(str(e))
db.close()
