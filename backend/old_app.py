from flask import Flask, render_template, jsonify, request
import pymysql

app = Flask(__name__, static_folder="./dist/static", template_folder="./dist")
db = pymysql.connect("localhost", "root", "11112222", "new_films", charset='utf8')
cursor = db.cursor()


@app.route('/api/getJsonInfo', methods=['GET'])
def random_number():
    start_index = int(request.args.get('start_index'))
    page_size = int(request.args.get('page_size'))
    movies = []
    try:
        cursor.execute('select * from main limit %d,%d' % (start_index, page_size))
        results = cursor.fetchall()
        for result in results:
            _id = result[0]
            cast_list = []
            country_list = []
            director_list = []
            genre_list = []
            language_list = []
            pubdate_list = []
            writer_list = []

            cursor.execute('select * from castsC where _id = %s' % _id)
            connections = cursor.fetchall()
            for connection in connections:
                cursor.execute('select * from casts where index_ = %s' % connection[1])
                value = cursor.fetchall()[0]
                cast_list.append({'id': value[1], 'name': value[2]})

            cursor.execute('select * from countriesC where _id = %s' % _id)
            connections = cursor.fetchall()
            for connection in connections:
                cursor.execute('select * from countries where index_ = %s' % connection[1])
                value = cursor.fetchall()[0]
                country_list.append(value[1])

            cursor.execute('select * from directorsC where _id = %s' % _id)
            connections = cursor.fetchall()
            for connection in connections:
                cursor.execute('select * from directors where index_ = %s' % connection[1])
                value = cursor.fetchall()[0]
                director_list.append({'id': value[1], 'name': value[2]})

            cursor.execute('select * from genresC where _id = %s' % _id)
            connections = cursor.fetchall()
            for connection in connections:
                cursor.execute('select * from genres where index_ = %s' % connection[1])
                value = cursor.fetchall()[0]
                genre_list.append(value[1])

            cursor.execute('select * from languagesC where _id = %s' % _id)
            connections = cursor.fetchall()
            for connection in connections:
                cursor.execute('select * from languages where index_ = %s' % connection[1])
                value = cursor.fetchall()[0]
                language_list.append(value[1])

            cursor.execute('select * from pubdateC where _id = %s' % _id)
            connections = cursor.fetchall()
            for connection in connections:
                cursor.execute('select * from pubdate where index_ = %s' % connection[1])
                value = cursor.fetchall()[0]
                pubdate_list.append(value[1])

            cursor.execute('select * from writersC where _id = %s' % _id)
            connections = cursor.fetchall()
            for connection in connections:
                cursor.execute('select * from writers where index_ = %s' % connection[1])
                value = cursor.fetchall()[0]
                writer_list.append({'id': value[1], 'name': value[2]})

            movie = {
                'ratingAverage': result[1],
                'ratingPeople': result[2],
                'star5': result[3],
                'star4': result[4],
                'star3': result[5],
                'star2': result[6],
                'star1': result[7],
                'title': result[8],
                'poster': result[9],
                'imdb': result[10],
                'year': result[11],
                'duration': result[12],
                'casts': cast_list,
                'countries': country_list,
                'directors': director_list,
                'genres': genre_list,
                'languages': language_list,
                'pubdate': pubdate_list,
                'writers': writer_list
            }
            print(movie)
            movies.append(movie)
    except Exception as e:
        db.rollback()
        print(str(e))
    db.close()
    return jsonify(movies)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
