#__author__ == "Jackie Cohen (jczetta)"

import os
from flask import Flask, render_template, session, redirect, url_for # tools that will make it easier to build on things
from flask_sqlalchemy import SQLAlchemy # handles database stuff for us - need to pip install flask_sqlalchemy in your virtual env, environment, etc to use this and run this

# Application configurations
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string for app security adgsdfsadfdflsdfsj'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./sample_movies.db' # TODO: decide what your new database name will be -- that has to go here
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Set up Flask debug stuff
db = SQLAlchemy(app) # For database use
session = db.session # to make queries easy





#########
######### Everything above this line is important/useful setup, not problem-solving.
#########


##### Set up Models #####

# Set up association Table between directors and albums
# collections = db.Table('collections',db.Column('album_id',db.Integer, db.ForeignKey('albums.id')),db.Column('director_id',db.Integer, db.ForeignKey('directors.id')))
#album_id is the foreign key that refers to the albums table. In the albums table, we are referring the id of the album.
#albums_id

#set up association with Movie and Directors
# collections = db.Table('collections',db.Column('movie_id',db.Integer, db.ForeignKey('movies.id')),db.Column('director_id',db.Integer, db.ForeignKey('directors.id')))

# class Album(db.Model):
#     __tablename__ = "albums"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64))
#     directors = db.relationship('Director',secondary=collections,backref=db.backref('albums',lazy='dynamic'),lazy='dynamic')
#     movies = db.relationship('Movie',backref='Album')

# class Director(db.Model):
#     __tablename__ = "directors"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64))
#     movies = db.relationship('Movie',backref='Director')
#
#     def __repr__(self):
#         return "{} (ID: {})".format(self.name,self.id)

# ************* DIRECTOR CLASS ********************
class Director(db.Model):
    __tablename__ = "directors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    movies = db.relationship('Movie',backref='Director')

    def __repr__(self):
        return "{} (ID: {})".format(self.name,self.id)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64),unique=True) # Only unique title movies can exist in this data model
    director_id = db.Column(db.Integer, db.ForeignKey("directors.id")) #ok to be null for now
    # collection_id = db.Column(db.Integer, db.ForeignKey("collections.id")) # ok to be null for now
    genre = db.Column(db.String(64)) # ok to be null
    # keeping genre as atomic element here even though in a more complex database it could be its own table and be referenced here

    def __repr__(self):
        return "{} by {} | {}".format(self.title,self.directors_id, self.genre)

# class Movie(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(64),unique=True) # Only unique title movies can exist in this data model
#     album_id = db.Column(db.Integer, db.ForeignKey("albums.id")) #ok to be null for now
#     director_id = db.Column(db.Integer, db.ForeignKey("directors.id")) # ok to be null for now
#     genre = db.Column(db.String(64)) # ok to be null
#     # keeping genre as atomic element here even though in a more complex database it could be its own table and be referenced here
#
#     def __repr__(self):
#         return "{} by {} | {}".format(self.title,self.director_id, self.genre)


##### Helper functions #####

### For database additions
### Relying on global session variable above existing


def get_or_create_director(director_name):
    director = Director.query.filter_by(name=director_name).first()
    if director:
        return director
    else:
        director = Director(name=director_name)
        session.add(director)
        session.commit()
        return director



##### Set up Controllers (route functions) #####

## Main route
@app.route('/')
def index():
    movies = Movie.query.all()
    num_movie = len(movies)
    return render_template('index.html', num_movie=num_movie)

@app.route('/movie/new/<title>/<director>/<genre>/')
def new_movie(title, director, genre):
    if Movie.query.filter_by(title=title).first(): # if there is a movie by that title
        return "That movie already exists! Go back to the main app!"
    else:
        director = get_or_create_director(director)
        movie = Movie(title=title, director_id=director.id,genre=genre)
        session.add(movie)
        session.commit()
        return "New movie: {} by {}. Check out the URL for ALL movies to see the whole list.".format(movie.title, director.name)

@app.route('/all_movies')
def see_all():
    all_movies = [] # Will be be tuple list of title, genre
    movies = Movie.query.all()
    for s in movies:
        director = Director.query.filter_by(id=s.director_id).first() # get just one director instance
        all_movies.append((s.title,director.name, s.genre)) # get list of movies with info to easily access [not the only way to do this]
    return render_template('all_movies.html',all_movies=all_movies) # check out template to see what it's doing with what we're sending!

@app.route('/all_directors')
def see_all_directors():
    directors = Director.query.all()
    names = []
    for a in directors:
        num_movies = len(Movie.query.filter_by(director_id=a.id).all())
        newtup = (a.name,num_movies)
        names.append(newtup) # names will be a list of tuples
    return render_template('all_directors.html',director_names=names)


if __name__ == '__main__':
    db.create_all() # This will create database in current directory, as set up, if it doesn't exist, but won't overwrite if you restart - so no worries about that
    app.run() # run with this: python main_app.py runserver
