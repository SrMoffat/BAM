from app.app import api
from app.app import SignUp


api.add_resource(SignUp, '/auth/signup')