import pymysql
import json

db = pymysql.connect("localhost", "root", "11112222", "new_films", charset='utf8')
cursor = db.cursor()
start_id = 0
search_length = 10

try:
    cursor.execute('select * from main limit()')
except Exception as e:
    db.rollback()
    print(str(e))
db.close()