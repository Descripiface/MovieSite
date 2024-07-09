from app import app,db
from flask import render_template,request,redirect,url_for
from flask_security import current_user
from models import *

from config import Configuration


POSTS_PER_PAGE = Configuration.POSTS_PER_PAGE

@app.route('/')
@app.route('/page=<int:page>')
def index(page=1):
    movies_banner = Movie.query.filter(Movie.rating_kinopoisk >= 7).all()[10:20]

    general = Movie.query.paginate(page, POSTS_PER_PAGE, False)
    generals = sorl_list(general.items)

    return render_template('index.html',movies_banner=movies_banner, generals=generals, general=general)


def sorl_list(movies):
    list_movie_ganre = []
    n = 0
    for sort in movies:
        if n == 0:
            list_movie_ganre.append([])
        if n == 6:
            list_movie_ganre.append([])
            n = 0
        list_movie_ganre[-1].append(sort)
        n +=1
    return list_movie_ganre


@app.route('/movie_<id_movie>')
def movie(id_movie):
    # if current_user.has_role('admin') == True:
    movies_banner = Movie.query.filter(Movie.rating_kinopoisk >= 7).all()[:10]

    movie = Movie.query.filter(Movie.id_movie == id_movie).first()
    return render_template('page_movie.html', movie=movie, movie_list=movies_banner)
    # else:
    #     return redirect(url_for('security.login', next=request.url))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        password = request.form['Password']
        email = request.form['Email']

        try:
            form_insert = User(email=email, password=password, active=1)
            db.session.add(form_insert)
            db.session.commit()

            return render_template('register.html', masege='Регистрация прошла цспешно')
        except:
            return redirect(url_for('security.login', next=request.url), masege='Вы уже зарегестрированы!')