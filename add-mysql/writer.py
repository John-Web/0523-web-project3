import pymysql
import json

db = pymysql.connect("localhost", "root", "11112222", "new_films", charset='utf8')
cursor = db.cursor()
cursor.execute("drop table if exists writers")
cursor.execute("drop table if exists writersC")

writers_create = """CREATE TABLE writers (
    index_ char(6) primary key,
    id char(20),
    name char(60)
)"""
writersC_create = """CREATE TABLE writersC (
    _id char(15),
    index_ char(6),
    primary key(_id,index_)
)"""

cursor.execute(writers_create)
cursor.execute(writersC_create)

writers_text = []
writersC_text = []
writers_textT = []
writers_re = "insert into writers(index_, id, name) values (%s, %s, %s)"
writersC_re = "insert into writersC(_id, index_) values (%s, %s)"

f = open('films_all.json', encoding='utf-8')
try:
    for i in range(0, 10000):
        if i % 100 == 0:
            print(u'正在载入第%s行......' % i)
        lines = f.readline()  # 使用逐行读取的方法
        j = json.loads(lines)  # 解析每一行数据

        for writer in j['writers']:
            index = 0
            while index < len(writers_text):
                if writers_text[index][0] == writer['id'] and writers_text[index][1] == writer['name']:
                    break
                index += 1
            if index == len(writers_text):
                writers_text.append((writer['id'], writer['name']))

            if not len(writersC_text):
                writersC_text.append((j['_id'], index))
            else:
                indexC = len(writersC_text) - 1
                while indexC >= 0 and writersC_text[indexC][0] == j['_id']:
                    if writersC_text[indexC][1] == index:
                        break
                    indexC -= 1
                if indexC == -1 or writersC_text[indexC][0] != j['_id']:
                    writersC_text.append((j['_id'], index))

    for writers_id in range(len(writers_text)):
        writers_textT.append((writers_id, writers_text[writers_id][0], writers_text[writers_id][1]))

    cursor.executemany(writers_re, writers_textT)
    db.commit()
    print("writers success!")
    cursor.executemany(writersC_re, writersC_text)
    db.commit()
    print("writersC success!")

except Exception as e:
    db.rollback()
    print(str(e))
db.close()

