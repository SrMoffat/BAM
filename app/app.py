from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, api, Resource, User

users = []


class SignUp(Resource):
    """
    The resource for user registration
    """
    def post(self):
        """
        The post method to create new user POST api/v1/auth/signup
        """
        # Get input in json
        username = request.json['username']
        password = request.json['password']

        # Check for null values for username and password
        if not username or not password:
            return {
                'status': 400,
                'message' : 'All fields required!'
            },400

        # Check for empty string values
        elif len(password.split()) == 0 or len(username.split()) == 0:
            return {
                'status' : 400,
                'message' : 'Invalid input!'
            }, 400

        # Check password length    
        elif len(password) < 6:
            return {
                'status' : 422,
                'message' : 'Password too weak!'
            }, 422

        hashed_password = generate_password_hash(password, method='sha256')

        # Block double entry
        for user in users:
            if username == user['username']:
                return {
                    'status' : 409,
                    'message' : 'Username already exists!'
                }, 409

        # Create user object
        new_user = User(username=username,
                        password=hashed_password,
                        admin=False)
        
        # Store the user object in user_holder
        new_user_holder = {}
        new_user_holder['username'] = username
        new_user_holder['password'] = hashed_password
        new_user_holder['admin'] = new_user.admin

        # Check for successful instantiation then add new_user to storage
        if new_user:
            users.append(new_user_holder) 
        else:
            return jsonify({
                'message' : 'User not created!'
            })

        return {
            'status' : 201,
            'message' : 'You have been succesfully registered!'
        }, 201

class Login(Resource):
    """
    The resource for user login
    """

    def post(self):
        """
        The post method to login user POST api/v1/auth/login
        """
   
        # Get input in json
        username = request.json['username']
        password = request.json['password']

        # Check for null values for username and password
        if not username or not password:
            return {
                'status': 400,
                'message' : 'All fields required!'
            },400

        # Check provided credentials against storage
        if username not in [user['username'] for user in users]:
            return {
                'status' : 403,
                'message' : 'Invalid credentials!'
            }, 403
        for user in users:
            if username == user['username'] and check_password_hash(user['password'], password):
                return {
                    'status' : 200,
                    'message' : 'You are now logged in!'
                }, 200


      