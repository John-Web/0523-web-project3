import pymysql
import json

db = pymysql.connect("localhost", "root", "11112222", "new_films", charset='utf8')
cursor = db.cursor()
cursor.execute("drop table if exists directors")
cursor.execute("drop table if exists directorsC")

directors_create = """CREATE TABLE directors (
    index_ char(6) primary key,
    id char(15),
    name char(60)
)"""
directorsC_create = """CREATE TABLE directorsC (
    _id char(15),
    index_ char(6),
    primary key(_id,index_)
)"""

cursor.execute(directors_create)
cursor.execute(directorsC_create)

directors_text = []
directorsC_text = []
directors_textT = []
directors_re = "insert into directors(index_, id, name) values (%s, %s, %s)"
directorsC_re = "insert into directorsC(_id, index_) values (%s, %s)"

f = open('films_all.json', encoding='utf-8')
try:
    for i in range(0, 10000):
        if i % 100 == 0:
            print(u'正在载入第%s行......' % i)
        lines = f.readline()  # 使用逐行读取的方法
        j = json.loads(lines)  # 解析每一行数据

        for director in j['directors']:
            index = 0
            while index < len(directors_text):
                if directors_text[index][0] == director['id'] and directors_text[index][1] == director['name']:
                    break
                index += 1
            if index == len(directors_text):
                directors_text.append((director['id'], director['name']))

            if not len(directorsC_text):
                directorsC_text.append((j['_id'], index))
            else:
                indexC = len(directorsC_text) - 1
                while indexC >= 0 and directorsC_text[indexC][0] == j['_id']:
                    if directorsC_text[indexC][1] == index:
                        break
                    indexC -= 1
                if indexC == -1 or directorsC_text[indexC][0] != j['_id']:
                    directorsC_text.append((j['_id'], index))

    for directors_id in range(len(directors_text)):
        directors_textT.append((directors_id, directors_text[directors_id][0], directors_text[directors_id][1]))

    cursor.executemany(directors_re, directors_textT)
    db.commit()
    print("directors success!")
    cursor.executemany(directorsC_re, directorsC_text)
    db.commit()
    print("directorsC success!")

except Exception as e:
    db.rollback()
    print(str(e))
db.close()
