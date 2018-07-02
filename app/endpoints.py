from app.app import api
from app.app import SignUp, Login, Meal


api.add_resource(SignUp, '/auth/signup')
api.add_resource(Login, '/auth/login')
api.add_resource(Meal, '/meals')