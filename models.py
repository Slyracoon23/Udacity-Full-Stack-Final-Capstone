from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgres://fnlcrowvinkpsl:8140266e4e0ea8572dd31131089023abbf13cd31e12efdab376bda2aace6d18c@ec2-52-207-25-133.compute-1.amazonaws.com:5432/d1j98vqtb2a02l' #os.environ['DATABASE_URL']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    #migrate = Migrate(app, db)
    db.init_app(app)


def db_drop_and_create_all():
    '''drops the database tables and starts fresh
    can be used to initialize a clean database
    '''
    db.drop_all()
    db.create_all()
    db_init_records()

def db_init_records():
    '''this will initialize the database with some test records.'''


    new_movie = (Movie(
        title = 'Matthew first Movie',
        release_date = '2020-05-30'
        ))
    new_movie2 = (Movie(
        title='Random Movie',
        release_date='2020-05-30'
    ))
    new_movie.insert()
    new_movie2.insert()
    db.session.commit()

    new_actor = (Actor(
        name='Matthew',
        gender='Male',
        age=25,
        movie_id= Movie.query.filter(Movie.title == "Matthew first Movie").one_or_none().id
    ))

    new_actor.insert()
    db.session.commit()





class Movie(db.Model):
    #this is the movie table in my database . It will have a one to many relationship with the actors table since there are many actors to one movie 
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.Date)
    actors = db.relationship('Actor', backref='movies')

    def format(self):
        return{
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actors': self.actors        
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Actor(db.Model):
    #this would be the actors table. It will be the child of the Movie table
    __tablename__ = 'actors' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movie_id': self.movie_id
        }
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
