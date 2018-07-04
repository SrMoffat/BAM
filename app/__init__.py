from flask import Flask 
from flask_restplus import Resource, Api
from config import app_config

app = Flask(__name__)
api = Api(app, 
         version='1.0',
         title='Book-A-Meal Restful API',
         description='Restful web service for booking meals',
         prefix='/api/v1')

app.config.from_object(app_config['testing'])


from app.models import User, MealOption, Menu
