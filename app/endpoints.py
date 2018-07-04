from app.app import api
from app.app import SignUp, Login, Meal, SingleMeal, Menu


api.add_resource(SignUp, '/auth/signup')
api.add_resource(Login, '/auth/login')
api.add_resource(Meal, '/meals')
api.add_resource(SingleMeal, '/meals/<int:id>')
api.add_resource(Menu, '/menu')