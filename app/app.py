from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, api, Resource, User


class SignUp(Resource):
    """
    The resource for user registration
    """
    def post(self):
        """
        The post method to create new user POST api/v1/auth/signup
        """
        username = request.json['username']
        password = request.json['password']

        if not username or not password:
            return {
                'status': 400,
                'message' : 'All fields required'
            },400

        return jsonify({
            'username' : username,
            'password' : password
        })
