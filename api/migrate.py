from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from db import db
from app import create_app

app = create_app('config')

