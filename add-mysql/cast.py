import pymysql
import json

db = pymysql.connect("localhost", "root", "11112222", "new_films", charset='utf8')
cursor = db.cursor()
cursor.execute("drop table if exists casts")
cursor.execute("drop table if exists castsC")

casts_create = """CREATE TABLE casts (
    index_ char(6) primary key,
    id char(15),
    name char(150)
)"""
castsC_create = """CREATE TABLE castsC (
    _id char(15),
    index_ char(6),
    primary key(_id,index_)
)"""

cursor.execute(casts_create)
cursor.execute(castsC_create)

casts_text = []
castsC_text = []
casts_textT = []
casts_re = "insert into casts(index_, id, name) values (%s, %s, %s)"
castsC_re = "insert into castsC(_id, index_) values (%s, %s)"

f = open('films_all.json', encoding='utf-8')
try:
    for i in range(0, 10000):
        if i % 100 == 0:
            print(u'正在载入第%s行......' % i)
        lines = f.readline()  # 使用逐行读取的方法
        j = json.loads(lines)  # 解析每一行数据

        for cast in j['casts']:
            index = 0
            while index < len(casts_text):
                if casts_text[index][0] == cast['id'] and casts_text[index][1] == cast['name']:
                    break
                index += 1
            if index == len(casts_text):
                casts_text.append((cast['id'], cast['name']))

            if not len(castsC_text):
                castsC_text.append((j['_id'], index))
            else:
                indexC = len(castsC_text) - 1
                while indexC >= 0 and castsC_text[indexC][0] == j['_id']:
                    if castsC_text[indexC][1] == index:
                        break
                    indexC -= 1
                if indexC == -1 or castsC_text[indexC][0] != j['_id']:
                    castsC_text.append((j['_id'], index))

    for casts_id in range(len(casts_text)):
        casts_textT.append((casts_id, casts_text[casts_id][0], casts_text[casts_id][1]))

    cursor.executemany(casts_re, casts_textT)
    db.commit()
    print("casts success!")
    cursor.executemany(castsC_re, castsC_text)
    db.commit()
    print("castsC success!")

except Exception as e:
    db.rollback()
    print(str(e))
db.close()
