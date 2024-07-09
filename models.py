from app import db
from datetime import datetime

from flask_security import UserMixin,RoleMixin


def data_time():
    d = datetime.now()
    return d

def generate_slug(unit):
    s = 'movie_' + str(unit)
    return s

movie_actors = db.Table('movie_actor',
                          db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
                          db.Column('actor_id', db.Integer, db.ForeignKey('actor.id')))

movie_genres = db.Table('movie_genre',
                          db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
                          db.Column('genre_id', db.Integer, db.ForeignKey('genre.id')))

movie_posters = db.Table('movie_posters',
                          db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
                          db.Column('poster_id', db.Integer, db.ForeignKey('poster.id')))

user_role = db.Table('user_role',
                          db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                          db.Column('role_id', db.Integer, db.ForeignKey('role.id')))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_movie = db.Column(db.Integer)
    year = db.Column(db.Integer, default=2019)
    title = db.Column(db.String(255))
    title_en = db.Column(db.String(255))
    tagline = db.Column(db.String(255))
    description = db.Column(db.Text())
    runtime = db.Column(db.Integer)
    actors = db.relationship('Actor', secondary=movie_actors, backref=db.backref('movie', lazy='dynamic'))
    genres = db.relationship('Genre', secondary=movie_genres, backref=db.backref('movie', lazy='dynamic'))
    rating_kinopoisk = db.Column(db.Float, default=0)
    rating_imdb = db.Column(db.Float, default=0)
    poster = db.relationship('Poster', secondary=movie_posters, backref=db.backref('movie', lazy='dynamic'))
    active = db.Column(db.String(100), default='off')
    created = db.Column(db.DateTime, default=data_time())

    def __init__(self, *args,**kwargs):
        super(Movie, self).__init__(*args,**kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.id_movie:
            self.slug = 'movie_' + str(self.id_movie)

    def __repr__(self):
        return 'Title: {}'.format(self.title)


class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return '{}'.format(self.name)

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))

    def __repr__(self):
        return '{}'.format(self.name)

class Poster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    path = db.Column(db.String(100), default='/static/image/')

    def __repr__(self):
        return '{}'.format(self.title)


class Role(db.Model,RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '{}'.format(self.name)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(),default='NULL')
    roles = db.relationship('Role', secondary=user_role, backref=db.backref('user', lazy='dynamic'))
