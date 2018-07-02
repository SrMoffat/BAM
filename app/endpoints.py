from app.app import api
from app.app import SignUp, Login


api.add_resource(SignUp, '/auth/signup')
api.add_resource(Login, '/auth/login')