from flask import jsonify, Flask
from utils import search_by_title, search_by_years, search_by_rating, search_by_genre

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def page_index():
    return '<h1>Привет</h1>'


@app.route('/movie/<title>')
def search(title):
    data = search_by_title(title)
    return jsonify(data)


@app.route('/movie/<int:year>/to/<int:last_year>')
def search_year(year, last_year):
    data = search_by_years(year, last_year)
    return jsonify(data)


@app.route('/rating/<group>')
def search_rating(group):
    levels = {
        'children': ['G'],
        'family': ['PG', 'G', 'PG-13'],
        'adult': ['R', 'NC-17']
    }
    if group in levels:
        level = '\", \"'.join(levels[group])
        level = f'\"{level}\"'
        data = search_by_rating(level)
        return jsonify(data)
    else:
        return jsonify([])


@app.route('/genre/<genre>')
def search_genre(genre):
    data = search_by_genre(genre)
    return jsonify(data)


if __name__ == "__main__":
    app.run()
