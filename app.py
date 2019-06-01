from flask import Flask, render_template, jsonify, request
import pymysql
import json

app = Flask(__name__, static_folder="./dist/static", template_folder="./dist")


@app.route('/api/all_movies', methods=['GET'])
def get_movies():
    db = pymysql.connect("localhost", "root", "11112222", "new_films", charset='utf8')
    cursor = db.cursor()
    start_index = int(request.args.get('start_index'))
    page_size = int(request.args.get('page_size'))
    movies = []
    try:
        cursor.execute('select * from main limit %d,%d' % (start_index, page_size))
        results = cursor.fetchall()
        for result in results:
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
                'casts': json.loads(result[13]),
                'countries': json.loads(result[14]),
                'directors': json.loads(result[15]),
                'genres': json.loads(result[16]),
                'languages': json.loads(result[17]),
                'pubdate': json.loads(result[18]),
                'writers': json.loads(result[19])
            }
            movies.append(movie)
    except Exception as e:
        db.rollback()
        print(str(e))
    db.close()
    return jsonify(movies)


@app.route('/api/search_movies', methods=['GET'])
def search_movies():
    db = pymysql.connect("localhost", "root", "11112222", "new_films", charset='utf8')
    cursor = db.cursor()
    search_text = request.args.get('search_text')
    movies = []
    length = 0
    id_list = []
    try:
        cursor.execute('select * from main where title like \'%%%s%%\'' % search_text)
        results = cursor.fetchall()
        for result in results:
            if result[0] not in id_list:
                id_list.append(result[0])
                length += 1
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
                    'casts': json.loads(result[13]),
                    'countries': json.loads(result[14]),
                    'directors': json.loads(result[15]),
                    'genres': json.loads(result[16]),
                    'languages': json.loads(result[17]),
                    'pubdate': json.loads(result[18]),
                    'writers': json.loads(result[19])
                }
                movies.append(movie)

        cursor.execute('select * from casts where name = \'%s\'' % search_text)
        results = cursor.fetchall()
        if len(results) != 0:
            index_ = results[0][0]
            cursor.execute('select * from castsC where index_ = \'%s\'' % index_)
            connection_results = cursor.fetchall()
            for connection in connection_results:
                _id = connection[0]
                if _id not in id_list:
                    id_list.append(_id)
                    length += 1
                    cursor.execute('select * from main where _id = \'%s\'' % _id)
                    movie_results = cursor.fetchall()
                    movie = {
                        'ratingAverage': movie_results[0][1],
                        'ratingPeople': movie_results[0][2],
                        'star5': movie_results[0][3],
                        'star4': movie_results[0][4],
                        'star3': movie_results[0][5],
                        'star2': movie_results[0][6],
                        'star1': movie_results[0][7],
                        'title': movie_results[0][8],
                        'poster': movie_results[0][9],
                        'imdb': movie_results[0][10],
                        'year': movie_results[0][11],
                        'duration': movie_results[0][12],
                        'casts': json.loads(movie_results[0][13]),
                        'countries': json.loads(movie_results[0][14]),
                        'directors': json.loads(movie_results[0][15]),
                        'genres': json.loads(movie_results[0][16]),
                        'languages': json.loads(movie_results[0][17]),
                        'pubdate': json.loads(movie_results[0][18]),
                        'writers': json.loads(movie_results[0][19])
                    }
                    movies.append(movie)

        cursor.execute('select * from directors where name = \'%s\'' % search_text)
        results = cursor.fetchall()
        if len(results) != 0:
            index_ = results[0][0]
            cursor.execute('select * from directorsC where index_ = \'%s\'' % index_)
            connection_results = cursor.fetchall()
            for connection in connection_results:
                _id = connection[0]
                if _id not in id_list:
                    id_list.append(_id)
                    length += 1
                    cursor.execute('select * from main where _id = \'%s\'' % _id)
                    movie_results = cursor.fetchall()
                    movie = {
                        'ratingAverage': movie_results[0][1],
                        'ratingPeople': movie_results[0][2],
                        'star5': movie_results[0][3],
                        'star4': movie_results[0][4],
                        'star3': movie_results[0][5],
                        'star2': movie_results[0][6],
                        'star1': movie_results[0][7],
                        'title': movie_results[0][8],
                        'poster': movie_results[0][9],
                        'imdb': movie_results[0][10],
                        'year': movie_results[0][11],
                        'duration': movie_results[0][12],
                        'casts': json.loads(movie_results[0][13]),
                        'countries': json.loads(movie_results[0][14]),
                        'directors': json.loads(movie_results[0][15]),
                        'genres': json.loads(movie_results[0][16]),
                        'languages': json.loads(movie_results[0][17]),
                        'pubdate': json.loads(movie_results[0][18]),
                        'writers': json.loads(movie_results[0][19])
                    }
                    movies.append(movie)

        cursor.execute('select * from writers where name = \'%s\'' % search_text)
        results = cursor.fetchall()
        if len(results) != 0:
            index_ = results[0][0]
            cursor.execute('select * from writersC where index_ = \'%s\'' % index_)
            connection_results = cursor.fetchall()
            for connection in connection_results:
                _id = connection[0]
                if _id not in id_list:
                    id_list.append(_id)
                    length += 1
                    cursor.execute('select * from main where _id = \'%s\'' % _id)
                    movie_results = cursor.fetchall()
                    movie = {
                        'ratingAverage': movie_results[0][1],
                        'ratingPeople': movie_results[0][2],
                        'star5': movie_results[0][3],
                        'star4': movie_results[0][4],
                        'star3': movie_results[0][5],
                        'star2': movie_results[0][6],
                        'star1': movie_results[0][7],
                        'title': movie_results[0][8],
                        'poster': movie_results[0][9],
                        'imdb': movie_results[0][10],
                        'year': movie_results[0][11],
                        'duration': movie_results[0][12],
                        'casts': json.loads(movie_results[0][13]),
                        'countries': json.loads(movie_results[0][14]),
                        'directors': json.loads(movie_results[0][15]),
                        'genres': json.loads(movie_results[0][16]),
                        'languages': json.loads(movie_results[0][17]),
                        'pubdate': json.loads(movie_results[0][18]),
                        'writers': json.loads(movie_results[0][19])
                    }
                    movies.append(movie)
    except Exception as e:
        db.rollback()
        print(str(e))
    db.close()
    return jsonify({'length': length, 'movies': movies})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
