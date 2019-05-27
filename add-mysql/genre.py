import pymysql
import json

db = pymysql.connect("localhost", "root", "11112222", "new_films", charset='utf8')
cursor = db.cursor()
cursor.execute("drop table if exists genres")
cursor.execute("drop table if exists genresC")

genres_create = """CREATE TABLE genres (
    index_ char(6) primary key,
    name char(10)
)"""
genresC_create = """CREATE TABLE genresC (
    _id char(15),
    index_ char(6),
    primary key(_id,index_)
)"""

cursor.execute(genres_create)
cursor.execute(genresC_create)

genres_text = []
genresC_text = []
genres_textT = []
genres_re = "insert into genres(index_, name) values (%s, %s)"
genresC_re = "insert into genresC(_id, index_) values (%s, %s)"

f = open('films_all.json', encoding='utf-8')
try:
    for i in range(0, 10000):
        if i % 100 == 0:
            print(u'正在载入第%s行......' % i)
        lines = f.readline()  # 使用逐行读取的方法
        j = json.loads(lines)  # 解析每一行数据

        for genre in j['genres']:
            index = 0
            while index < len(genres_text):
                if genres_text[index] == genre:
                    break
                index += 1
            if index == len(genres_text):
                genres_text.append(genre)
            genresC_text.append((j['_id'], index))

    for genres_id in range(len(genres_text)):
        genres_textT.append((genres_id, genres_text[genres_id]))

    cursor.executemany(genres_re, genres_textT)
    db.commit()
    print("genres success!")
    cursor.executemany(genresC_re, genresC_text)
    db.commit()
    print("genresC success!")

except Exception as e:
    db.rollback()
    print(str(e))
db.close()
