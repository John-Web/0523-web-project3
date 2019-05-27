import pymysql
import json

db = pymysql.connect("localhost", "root", "11112222", "new_films", charset='utf8')
cursor = db.cursor()
cursor.execute("drop table if exists countries")
cursor.execute("drop table if exists countriesC")

countries_create = """CREATE TABLE countries (
    index_ char(6) primary key,
    name char(40)
)"""
countriesC_create = """CREATE TABLE countriesC (
    _id char(15),
    index_ char(6),
    primary key(_id,index_)
)"""

cursor.execute(countries_create)
cursor.execute(countriesC_create)

countries_text = []
countriesC_text = []
countries_textT = []
countries_re = "insert into countries(index_, name) values (%s, %s)"
countriesC_re = "insert into countriesC(_id, index_) values (%s, %s)"

f = open('films_all.json', encoding='utf-8')
try:
    for i in range(0, 10000):
        if i % 100 == 0:
            print(u'正在载入第%s行......' % i)
        lines = f.readline()  # 使用逐行读取的方法
        j = json.loads(lines)  # 解析每一行数据

        for country in j['countries']:
            index = 0
            while index < len(countries_text):
                if countries_text[index] == country:
                    break
                index += 1
            if index == len(countries_text):
                countries_text.append(country)
            countriesC_text.append((j['_id'], index))

    for country_id in range(len(countries_text)):
        countries_textT.append((country_id, countries_text[country_id]))

    cursor.executemany(countries_re, countries_textT)
    db.commit()
    print("countries success!")
    cursor.executemany(countriesC_re, countriesC_text)
    db.commit()
    print("countriesC success!")

except Exception as e:
    db.rollback()
    print(str(e))
db.close()
