import pymysql
import json

db = pymysql.connect("localhost", "root", "11112222", "new_films", charset='utf8')
cursor = db.cursor()
cursor.execute("drop table if exists pubdate")
cursor.execute("drop table if exists pubdateC")

pubdate_create = """CREATE TABLE pubdate (
    index_ char(6) primary key,
    date char(60)
)"""
pubdateC_create = """CREATE TABLE pubdateC (
    _id char(15),
    index_ char(6),
    primary key(_id,index_)
)"""

cursor.execute(pubdate_create)
cursor.execute(pubdateC_create)

pubdate_text = []
pubdateC_text = []
pubdate_textT = []
pubdate_re = "insert into pubdate(index_, date) values (%s, %s)"
pubdateC_re = "insert into pubdateC(_id, index_) values (%s, %s)"

f = open('films_all.json', encoding='utf-8')
try:
    for i in range(0, 10000):
        if i % 100 == 0:
            print(u'正在载入第%s行......' % i)
        lines = f.readline()  # 使用逐行读取的方法
        j = json.loads(lines)  # 解析每一行数据

        for pubdate in j['pubdate']:
            index = 0
            while index < len(pubdate_text):
                if pubdate_text[index] == pubdate:
                    break
                index += 1
            if index == len(pubdate_text):
                pubdate_text.append(pubdate)
            pubdateC_text.append((j['_id'], index))

    for pubdate_id in range(len(pubdate_text)):
        pubdate_textT.append((pubdate_id, pubdate_text[pubdate_id]))

    cursor.executemany(pubdate_re, pubdate_textT)
    db.commit()
    print("pubdate success!")
    cursor.executemany(pubdateC_re, pubdateC_text)
    db.commit()
    print("pubdateC success!")

except Exception as e:
    db.rollback()
    print(str(e))
db.close()
