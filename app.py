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
    try:
        cursor.execute('select * from main where title ==  %s' % search_text)
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
            length += 1
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
    app.run()
