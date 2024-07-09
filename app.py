from flask import Flask,redirect,url_for,request
from config import Configuration
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView

from flask_security import SQLAlchemyUserDatastore
from flask_security import Security


app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)

migrate = Migrate(app, db)   # Подключаем механизм Миграции базы данных
manager = Manager(app)      # Подключаем менеджера Миграции базы данных
manager.add_command('db',MigrateCommand)


import view
from models import *
db.create_all()

# class HomeAdminView(AdminIndexView):
#     def is_accessible(self):
#         return current_user.has_role('admin')
#
#     def inaccessible_callback(self, name, **kwargs):
#         return redirect(url_for('security.login', next=request.url))

admin = Admin(app,'FlaskApp',url='/', index_view=AdminIndexView(name='Home'))
admin.add_view(ModelView(Movie, db.session))
admin.add_view(ModelView(Actor, db.session))
admin.add_view(ModelView(Genre, db.session))
admin.add_view(ModelView(Poster, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Role, db.session))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app,user_datastore)