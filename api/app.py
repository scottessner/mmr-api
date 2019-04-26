from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS
from db import db
from ma import ma
from flask_migrate import Migrate


from resources.movie import Movie, MovieList
from resources.disc import Disc, DiscList, DiscScan
from resources.title import Title, TitleList, TitleQuery
from resources.task import Task, TaskList, NextTask, TasksByTitle
from resources.status import TaskStatus

app = Flask(__name__)
migrate = Migrate(app, db)
# cors = CORS(app, resources={r"/mmr-api/*": {"origins": "*"}})
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///db/mmr-api.db'
app.secret_key = 'ernie'
api = Api(app, prefix='/v1')


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(MovieList, '/movies')
api.add_resource(Movie, '/movies/<int:_id>')
api.add_resource(DiscList, '/discs')
api.add_resource(Disc, '/discs/<int:_id>')
api.add_resource(DiscScan, '/discs/scan')
api.add_resource(TaskList, '/tasks')
api.add_resource(Task, '/tasks/<int:_id>')
api.add_resource(NextTask, '/tasks/next')
api.add_resource(TitleList, '/titles')
api.add_resource(Title, '/titles/<int:_id>')
api.add_resource(TitleQuery, '/titles/search')
api.add_resource(TasksByTitle, '/titles/<int:title_id>/tasks')
api.add_resource(TaskStatus, '/status/tasks')

db.init_app(app)

print("Name is: {}".format(__name__))
#
# if __name__ == '__main__':
#     from db import db
#     db.init_app(app)
#     app.run()
