from mysql import connector
import requests
import sqlite3
import json
from datetime import datetime

host = '127.0.0.1'
user = 'root'
password = '1'
database_x = 'kinopoisk'
database_y = 'movie_site'

class MysqlKinopoisk_x():
    def __init__(self):
        self.connect_x = connector.connect(host=host,
                                            user=user,
                                            password=password,
                                            database=database_x)

    def zapros_x(self,zapros):
        cursor = self.connect_x.cursor()
        cursor.execute(zapros)
        rows = cursor.fetchall()
        return rows

class SqlLite_connect():
    def __init__(self):
        self.conn = sqlite3.connect("app.db")
        self.cursor = self.conn.cursor()

    def movie(self,movie):
        self.cursor.execute(movie)
        self.conn.commit()

        return self.cursor.lastrowid


    def actor(self,actor,movie_id):
        sql_select = "SELECT * FROM actor WHERE name=?"
        self.cursor.execute(sql_select, [(actor)])
        otvet = self.cursor.fetchall()

        if otvet == []:
            sql_insert = 'INSERT INTO `actor`(`name`) VALUES ("{}")'.format(actor)
            self.cursor.execute(sql_insert)
            actor_id = self.cursor.lastrowid
        else:
            actor_id = otvet[0][0]

        sql_insert_ma = 'INSERT INTO `movie_actor`(`movie_id`, `actor_id`) VALUES ({},{})'.format(movie_id,actor_id)
        self.cursor.execute(sql_insert_ma)
        self.conn.commit()


    def ganre(self,genre,movie_id):
        sql_select = "SELECT * FROM genre WHERE name=?"
        self.cursor.execute(sql_select, [(genre)])
        otvet = self.cursor.fetchall()

        if otvet == []:
            sql_insert = 'INSERT INTO `genre`(`name`) VALUES ("{}")'.format(genre)
            self.cursor.execute(sql_insert)
            genre_id = self.cursor.lastrowid
        else:
            genre_id = otvet[0][0]

        sql_insert_ma = 'INSERT INTO `movie_genre`(`movie_id`, `genre_id`) VALUES ({},{})'.format(movie_id, genre_id)
        self.cursor.execute(sql_insert_ma)
        self.conn.commit()

    def poster(self,art,title,movie_id):
        sql_insert = 'INSERT INTO `poster`(`title`, `path`) VALUES ("{}","{}")'.format(title, '/static/image/movie_' + str(art) + '.jpg')
        self.cursor.execute(sql_insert)
        poster_id = self.cursor.lastrowid

        sql_insert_ma = 'INSERT INTO `movie_posters`(`movie_id`, `poster_id`) VALUES ({},{})'.format(movie_id, poster_id)
        self.cursor.execute(sql_insert_ma)
        self.conn.commit()



    def save_img(self,url,name):
        r = requests.get(url)
        out = open(name, "wb")
        out.write(r.content)
        out.close()




def main():
    SQL_SELECT = 'SELECT * FROM `movie_description` WHERE `year`= 2019'
    K = MysqlKinopoisk_x()
    resp = K.zapros_x(SQL_SELECT)
    A = SqlLite_connect()
    for r in resp:
        print(r)
        if 'сериал' in r[3]:
            continue
        # sql_insert_movie = "INSERT INTO `movie`(`id_movie`, `year`, `title`, `title_en`, `tagline`,`description`, `runtime`, `rating_kinopoisk`, `rating_imdb`,`active`,`created`) VALUES ({},{},'{}','{}','{}','{}',{},{},{},'{}','{}')".format(r[1],r[2],r[3],r[4],r[7],r[5],r[6],r[24],r[26],'off',datetime.now())
        # print(sql_insert_movie)
        # movie_id = A.movie(sql_insert_movie)
        #
        # actors = r[9].strip('[]').split(',')
        # for a in actors:
        #     actor = a.strip().strip('`')
        #     A.actor(actor,movie_id)
        #
        # genres = r[17].strip('[]').split(',')
        # for g in genres:
        #     genre = g.strip().strip('`')
        #     A.ganre(genre, movie_id)
        #
        # A.poster(r[1],r[3],movie_id)
        url = 'https://www.kinopoisk.ru/images/film_big/{}.jpg'.format(r[1])
        name = 'static/image/movie_' + str(r[1]) + '.jpg'
        A.save_img(url, name)





if __name__ == '__main__':
    main()

