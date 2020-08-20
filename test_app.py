import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from models import Actor, Movie, setup_db, db_drop_and_create_all
from app import create_app
from models import db
import datetime


casting_director_auth_header = {
    'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJEbG5pelUyVVA2RjJiajdsWXI2QSJ9.eyJpc3MiOiJodHRwczovL2Rldi0xYjFrMWl4ei51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTI2MTc2NjM0MjUxODI4NDk3NTMiLCJhdWQiOlsiY2FzdGluZy1jYXBzdG9uZSIsImh0dHBzOi8vZGV2LTFiMWsxaXh6LnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1OTc4ODExNTgsImV4cCI6MTU5Nzk2NzU1OCwiYXpwIjoiV1VkaTlsOTJHT0thQ1V6cVJhMm00M1hNNVBBWlR3WXciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9ycyIsImNyZWF0ZTptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImVkaXQ6YWN0b3JzIiwiZWRpdDptb3ZpZXMiLCJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.qYu5wsJg04uioEcJTEbCIQUCMyVkOiEUYmsKUaPOJv30TCM7-X-3axTQoMkUnYTW28GPhe3iWR5xVE2XnxmyRr5gFz1AI-8DS4hvYJcbpYI7phViM1-t64GO22M03XeCAVnddVsupsftE2vJfDcMuCAwGiBqBzeh12Abb1bCnTbO-TbqczX9Ydbr-y8_lz7W96f3uj8LnCJA8BCADu5TFiFp3LHxk5OrZjuRcPQaDcTXUO5vU3L7jhfMl5kwkJFlB1MIAvmvHZFg15V2er8OTqayyzSM9R5FxJ2uk5kpMzdyfUzH9-gtaDZ_MUSRyqRaycmnVX4-0GxsZilnYJVQ4g"
}

executive_producer_auth_header = {
    'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InJEbG5pelUyVVA2RjJiajdsWXI2QSJ9.eyJpc3MiOiJodHRwczovL2Rldi0xYjFrMWl4ei51cy5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTI2MTc2NjM0MjUxODI4NDk3NTMiLCJhdWQiOlsiY2FzdGluZy1jYXBzdG9uZSIsImh0dHBzOi8vZGV2LTFiMWsxaXh6LnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1OTc4ODExNTgsImV4cCI6MTU5Nzk2NzU1OCwiYXpwIjoiV1VkaTlsOTJHT0thQ1V6cVJhMm00M1hNNVBBWlR3WXciLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9ycyIsImNyZWF0ZTptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImVkaXQ6YWN0b3JzIiwiZWRpdDptb3ZpZXMiLCJ2aWV3OmFjdG9ycyIsInZpZXc6bW92aWVzIl19.qYu5wsJg04uioEcJTEbCIQUCMyVkOiEUYmsKUaPOJv30TCM7-X-3axTQoMkUnYTW28GPhe3iWR5xVE2XnxmyRr5gFz1AI-8DS4hvYJcbpYI7phViM1-t64GO22M03XeCAVnddVsupsftE2vJfDcMuCAwGiBqBzeh12Abb1bCnTbO-TbqczX9Ydbr-y8_lz7W96f3uj8LnCJA8BCADu5TFiFp3LHxk5OrZjuRcPQaDcTXUO5vU3L7jhfMl5kwkJFlB1MIAvmvHZFg15V2er8OTqayyzSM9R5FxJ2uk5kpMzdyfUzH9-gtaDZ_MUSRyqRaycmnVX4-0GxsZilnYJVQ4g"
}




class CastingTestCase(unittest.TestCase):

    def setUp(self):
        '''define test variables and initialize app'''

        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)
        db.create_all()
        db_drop_and_create_all()

        self.new_movie = {
            'title': 'New Movie',
            'release_date' : datetime.date(2019, 3, 13),
        }

        self.new_actor = {
            'name': 'John Doe',
            'age': 22,
            'gender': 'Male',
            'movie_id': Movie.query.filter(Movie.title == "Matthew first Movie").one_or_none().id
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        pass

    def test_get_healthy(self):
        res = self.client().get('/', headers = executive_producer_auth_header)
        self.assertEqual(res.status_code, 200)

    def test_get_movies(self):
        res = self.client().get('/movies',  headers = executive_producer_auth_header)
        self.assertEqual(res.status_code, 200)

    def test_get_movies_fail(self):
        res = self.client().get('/moviess', headers = executive_producer_auth_header)
        self.assertEqual(res.status_code, 404)

    def test_get_actors(self):
        res = self.client().get('/actors', headers = executive_producer_auth_header)
        self.assertEqual(res.status_code, 200)

    def test_get_actors_fail(self):
        res = self.client().get('/actorss', headers = executive_producer_auth_header)
        self.assertEqual(res.status_code, 404)

    def test_create_movie(self):
        res = self.client().post('/movies/create', json=self.new_movie,  headers = executive_producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_movie']['title'], 'New Movie')

    def test_create_actor(self):
        Movie.query.filter(Movie.title == "Matthew first Movie").one_or_none().id
        res = self.client().post('/actors/create', json=self.new_actor,  headers = executive_producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_actor']['name'], 'John Doe')
    
    def test_delete_movie(self):
        movie_id = Movie.query.filter(Movie.title == "Random Movie").one_or_none().id
        res = self.client().delete(f'/movies/delete/{movie_id}',  headers = executive_producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_delete_movie_fail(self):
        res = self.client().delete('/movies/delete/1000' ,  headers = executive_producer_auth_header)
        self.assertEqual(res.status_code, 404)
    
    def test_delete_actor(self):
        actor_id = Actor.query.filter(Actor.name == "Matthew").one_or_none().id
        res = self.client().delete(f'/actors/delete/{actor_id}',  headers = executive_producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_delete_actor_fail(self):
        res = self.client().delete('/actors/delete/1000',  headers = executive_producer_auth_header)
        self.assertEqual(res.status_code, 404)
    
    def test_patch_movie(self):
        movie_id = Movie.query.filter(Movie.title == "Random Movie").one_or_none().id
        res = self.client().patch(f'/movies/patch/{movie_id}', json=self.new_movie,  headers = executive_producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_patch_movie_fail(self):
        res = self.client().patch('/movies/patch/2000', json=self.new_movie,  headers = executive_producer_auth_header)
        self.assertEqual(res.status_code, 404)

    
    def test_patch_actor(self):
        actor_id = Actor.query.filter(Actor.name == "Matthew").one_or_none().id
        res = self.client().patch(f'/actors/patch/{actor_id}', json=self.new_actor,  headers = executive_producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_patch_actor_fail(self):
        res = self.client().patch('/actors/patch/2000', json=self.new_actor,  headers = executive_producer_auth_header)
        self.assertEqual(res.status_code, 404)
    






if __name__ == "__main__":
    unittest.main()

