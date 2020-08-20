import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from models import setup_db, Movie, Actor, db
from auth import AuthError, requires_auth


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app, resources={r"/api/": {"origins": "*"}})
  setup_db(app)

  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
      response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
      return response

  @app.route('/')
  #@requires_auth('view:actors')
  def get_health_check():
      print(request.endpoint)
      return render_template('index.html')

  @app.route('/callback')
  # @requires_auth('view:actors')
  def get_token():
      token_id = request.url
      print(token_id)
      return render_template('index.html')


  @app.route('/movies')
  #@requires_auth('view:movies')
  def get_movies():
      movies = Movie.query.all()
      movies = [movie.format() for movie in movies]
      for movie in movies:
        movie['actors'] = [i.format() for i in movie['actors']]
      return render_template('index.html', movies=movies )
  
  @app.route('/actors')
  #@requires_auth('view:actors')
  def get_actors():
      actors = Actor.query.all()
      actors = [actor.format() for actor in actors]
      return render_template('index.html', actors=actors )

  @app.route('/movies/create', methods=['POST'])
  @requires_auth('create:movies')
  def post_new_movie(payload):
      body = request.get_json()

      title = body.get('title', None)
      release_date = body.get('release_date', None)

      movie = Movie(title=title, release_date=release_date)
      movie.insert()
      new_movie = Movie.query.get(movie.id)
      new_movie = new_movie.format()

      return jsonify({
        'success': True,
        'created': movie.id,
        'new_movie': new_movie
      })

  @app.route('/actors/create', methods=['POST'])
  @requires_auth('create:actors')
  def post_new_actor(payload):
      body = request.get_json()
      name = body.get('name', None)
      age = body.get('age', None)
      gender = body.get('gender', None)
      movie_id = body.get('movie_id', None)

      actor = Actor(name=name, age=age, gender=gender, movie_id=movie_id)
      actor.insert()
      new_actor = Actor.query.get(actor.id)
      new_actor = new_actor.format()

      return jsonify({
        'success': True,
        'created': actor.id,
        'new_actor': new_actor
      })

  @app.route('/movies/delete/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(payload, movie_id):
      movie_to_delete = Movie.query.filter(Movie.id == movie_id).one_or_none()
      if not movie_to_delete:
          abort(404, {'message': 'Movie with id {} not found in database.'.format(movie_id)})
      movie_to_delete.delete()
      db.session.close()
      return jsonify({
        "success": True,
        "message" : "Delete occured"
      })

  @app.route('/actors/delete/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, actor_id):
      actor_to_delete = Actor.query.filter(Actor.id == actor_id).one_or_none()
      if not actor_to_delete:
          abort(404, {'message': 'Actor with id {} not found in database.'.format(actor_id)})
      actor_to_delete.delete()
      db.session.close()
      return jsonify({
        "success": True,
        "message" : "Delete occured"
      })

  @app.route('/actors/patch/<int:actor_id>', methods=['PATCH'])
  @requires_auth('edit:actors')
  def patch_actor(payload, actor_id):

      actor = Actor.query.filter(Actor.id== actor_id).one_or_none()
      if not actor:
          abort(404, {'message': 'Actor with id {} not found in database.'.format(actor_id)})
      body = request.get_json()
      name = body.get('name', None)
      age = body.get('age', None)
      gender = body.get('gender', None)
      movie_id = body.get('movie_id', None)
      actor.name = name
      actor.age = age
      actor.gender = gender
      actor.movie_id = movie_id
      actor.update()
      return jsonify({
        "success": True,
        "message": "update occured"
      })
    
  @app.route('/movies/patch/<int:movie_id>',methods=['PATCH'])
  @requires_auth('edit:movies')
  def patch_movie(payload,movie_id):
      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
      if not movie:
          abort(404, {'message': 'Movie with id {} not found in database.'.format(movie_id)})
      body = request.get_json()
      title = body.get('title', None)
      release_date = body.get('release_date', None)
      movie.title = title
      movie.release_date = release_date
      movie.update()
      return jsonify({
        "success": True,
        "message": "update occured"
      })

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
        'success': False,
        'error' : 404,
        'message' : 'Not Found'
      }), 404

  @app.errorhandler(422)
  def unprocessable_entity(error):
      return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable Entity'
      })      


  return app

app = create_app()




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)