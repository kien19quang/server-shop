from flask import Flask
from flask_pymongo import PyMongo
from app.config import Config
from flask_cors import CORS
from redis import Redis

mongo = PyMongo()
redis_client = Redis(host='localhost', port=6379, db=0)

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)

  mongo.init_app(app=app)

  CORS(app)

  from app.routes import register_routes

  register_routes(app=app)

  return app