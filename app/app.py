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

        # Create user object
        new_user = User(username=username,
                        password=password,
                        admin=False)
        
        # Store the user object in user_holder
        new_user_holder = {}
        new_user_holder['username'] = username
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
