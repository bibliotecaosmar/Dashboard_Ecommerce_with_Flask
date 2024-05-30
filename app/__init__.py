from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_script import Manager
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
migrate = Migrate(app, db)

#manager = Manager(app)
#manager.add_command('db', MigrateCommand)

from app.controllers import default



