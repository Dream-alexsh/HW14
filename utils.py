import sqlite3


def search_by_title(movie):
    with sqlite3.connect('netflix.db') as connect:
        cursor = connect.cursor()
        sqlite_query = f"""
                    SELECT title, country, MAX(release_year), listed_in, description
                    FROM netflix
                    WHERE title LIKE '%{movie}%'
                    AND type = 'Movie'
            """
        cursor.execute(sqlite_query)
        executed_query = cursor.fetchall()
        movie_dict = {
            'title': executed_query[0][0],
            'country': executed_query[0][1],
            'release_year': executed_query[0][2],
            'listed_in': executed_query[0][3],
            'description': executed_query[0][4].strip()
            }
        return movie_dict


def search_by_years(first, last):
    with sqlite3.connect('netflix.db') as connect:
        cursor = connect.cursor()
        results_list = []
        for year in range(first, last+1):

            sqlite_query = f"""
                            SELECT title, release_year
                            FROM netflix
                            WHERE release_year = {year}
                            LIMIT 100
                """
            cursor.execute(sqlite_query)
            executed_query = cursor.fetchall()

            years_dict = {'release_year': year}

            titles_str = ''
            for movie in executed_query:
                titles_str += movie[0] + ', '
            years_dict['title'] = titles_str
            results_list.append(years_dict)
        return results_list


def search_by_rating(rating):
    with sqlite3.connect('netflix.db') as connect:
        cursor = connect.cursor()
        results_list = []
        sqlite_query = f"""
                        SELECT title, rating, description
                        FROM netflix
                        WHERE rating IN ({rating})
                        LIMIT 10
                """
        cursor.execute(sqlite_query)
        executed_query = cursor.fetchall()
        for film in executed_query:
            rating_dict = {
                'title': film[0],
                'rating': film[1],
                'description': film[2].strip()
                }
            results_list.append(rating_dict)

        return results_list


def search_by_genre(genre):
    with sqlite3.connect('netflix.db') as connect:
        cursor = connect.cursor()
        results_list = []
        sqlite_query = f"""
                    SELECT title, description
                    FROM netflix
                    WHERE listed_in LIKE '%{genre}%'
                    AND type = 'Movie'
                    ORDER BY 'release_year' DESC
                    LIMIT 10 
              """
        cursor.execute(sqlite_query)
        executed_query = cursor.fetchall()
        for i in executed_query:
            movie_dict = {
                'title': i[0],
                'description': i[1].strip('\n')
                }
            results_list.append(movie_dict)
        return results_list


def casting(one, two):
    with sqlite3.connect('netflix.db') as connect:
        cursor = connect.cursor()
        sqlite_query = f"""
                    SELECT DISTINCT netflix.cast
                    FROM netflix
                    WHERE netflix.cast LIKE '%{one}%'
                    AND netflix.cast LIKE '%{two}%'
              """
        cursor.execute(sqlite_query)
        executed_query = cursor.fetchall()
        results_list = []
        for i in executed_query:
            results_list.extend(i[0].split(', '))
        actors = []
        for actor in results_list:
            if actor not in [one, two]:
                if results_list.count(actor) > 2:
                    actors.append(actor)
        actors = set(actors)
        return actors


def type_movie(movie, release_year, genre):
    with sqlite3.connect('netflix.db') as connect:
        cursor = connect.cursor()
        sqlite_query = f"""
                    SELECT title, description
                    FROM netflix
                    WHERE netflix.type = '{movie}'
                    AND release_year = '{release_year}'
                    AND listed_in LIKE '%{genre}%'
              """
        cursor.execute(sqlite_query)
        executed_query = cursor.fetchall()
        results_list = []
        for i in executed_query:
            movie_dict = {
                'title': i[0],
                'description': i[1].strip('\n')
                }
            results_list.append(movie_dict)
        return results_list


print(casting('Rose McIver', 'Ben Lamb'))
print(type_movie('Movie', 2018, 'Thrillers'))

