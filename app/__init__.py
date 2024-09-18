from flask import Flask
from flask_pymongo import PyMongo
from app.config import Config
from flask_cors import CORS
from redis import Redis
import os
from dotenv import load_dotenv

load_dotenv()

# Lấy các biến môi trường
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_db = int(os.getenv('REDIS_DB', 0))


mongo = PyMongo()
redis_client = Redis(host=redis_host, port=redis_port, db=redis_db)

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)

  mongo.init_app(app=app)

  CORS(app)

  from app.routes import register_routes

  register_routes(app=app)

  return app