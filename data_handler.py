from psycopg2 import sql
import connection


@connection.connection_handler
def get_shows(cursor):
    cursor.execute(sql.SQL("SELECT id, title "
                           "FROM shows"))
    return cursor.fetchall()


@connection.connection_handler
def get_most_rated_shows(cursor, offset, column, order):
    cursor.execute(sql.SQL("""SELECT shows.id, shows.title, shows.year, shows.runtime, CAST(ROUND(shows.rating, 1) as varchar) AS rating, shows.trailer, shows.homepage, STRING_AGG(genres.name, ', ') AS genres
    FROM shows
    JOIN show_genres ON show_genres.show_id = shows.id
    JOIN genres ON genres.id = show_genres.genre_id
    GROUP BY shows.id, shows.title, shows.year, shows.rating, shows.trailer, shows.homepage, shows.runtime
    ORDER BY shows.{column} {order}
    LIMIT 15
    OFFSET {offset}""").format(offset=sql.Literal(offset), column=sql.Identifier(column), order=sql.SQL(order)))
    return cursor.fetchall()


@connection.connection_handler
def show_detailed_view(cursor, id):
    cursor.execute(sql.SQL("""SELECT shows.id, shows.title, shows.overview, shows.runtime, STRING_AGG(DISTINCT genres.name, ', ') AS genres,
    CAST(ROUND(shows.rating, 1) as varchar) AS rating, shows.trailer, STRING_AGG(DISTINCT actors.name, ', ') AS actors
    FROM show_characters
    FULL OUTER JOIN shows ON shows.id = show_characters.show_id
    LEFT JOIN show_genres ON show_genres.show_id = shows.id
    LEFT JOIN genres ON genres.id = show_genres.genre_id
    LEFT JOIN actors ON show_characters.actor_id = actors.id
    GROUP BY shows.id, show_characters.show_id
    HAVING shows.id = {id}""").format(id=sql.Literal(id)))
    return cursor.fetchall()


@connection.connection_handler
def most_active_stars(cursor, id):
    cursor.execute(sql.SQL("""SELECT string_agg( distinct actors.name, ',') AS actors
    FROM actors
    LEFT JOIN show_characters ON actors.id = show_characters.actor_id
    WHERE show_characters.show_id = {id}
    GROUP BY show_characters.id
    ORDER BY show_characters.id
    LIMIT 3""").format(id=sql.Literal(id)))
    return cursor.fetchall()

@connection.connection_handler
def get_season(cursor, id):
    cursor.execute(sql.SQL("""SELECT seasons.title, seasons.overview, season_number
    FROM seasons
    LEFT JOIN shows on seasons.show_id = shows.id
    WHERE shows.id = {id}
    ORDER BY season_number""").format(id=sql.Literal(id)))
    return cursor.fetchall()


