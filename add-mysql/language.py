import pymysql
import json

db = pymysql.connect("localhost", "root", "11112222", "new_films", charset='utf8')
cursor = db.cursor()
cursor.execute("drop table if exists languages")
cursor.execute("drop table if exists languagesC")

languages_create = """CREATE TABLE languages (
    index_ char(6) primary key,
    name char(40)
)"""
languagesC_create = """CREATE TABLE languagesC (
    _id char(15),
    index_ char(6),
    primary key(_id,index_)
)"""

cursor.execute(languages_create)
cursor.execute(languagesC_create)

languages_text = []
languagesC_text = []
languages_textT = []
languages_re = "insert into languages(index_, name) values (%s, %s)"
languagesC_re = "insert into languagesC(_id, index_) values (%s, %s)"

f = open('films_all.json', encoding='utf-8')
try:
    for i in range(0, 10000):
        if i % 100 == 0:
            print(u'正在载入第%s行......' % i)
        lines = f.readline()  # 使用逐行读取的方法
        j = json.loads(lines)  # 解析每一行数据

        for language in j['languages']:
            index = 0
            while index < len(languages_text):
                if languages_text[index] == language:
                    break
                index += 1
            if index == len(languages_text):
                languages_text.append(language)
            languagesC_text.append((j['_id'], index))

    for language_id in range(len(languages_text)):
        languages_textT.append((language_id, languages_text[language_id]))

    cursor.executemany(languages_re, languages_textT)
    db.commit()
    print("languages success!")
    cursor.executemany(languagesC_re, languagesC_text)
    db.commit()
    print("languagesC success!")

except Exception as e:
    db.rollback()
    print(str(e))
db.close()
