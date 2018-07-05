from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, api, Resource, User, MealOption, MenuObj

users = []
meals = []
menus = []


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
        new_user_holder['id'] = new_user._ID
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

    def get(self):
        """
        Get all users --> Should be Admin Only
        """
        #Check if there are no users
        if len(users) == 0:
            return {
                'status' : 404,
                'users' : 'No users found!'
            }, 404
        else:
            return {
                'status' : 200,
                'no. of users' : len(users),
                'users' : users
            }, 200


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

        # Validate input then log user in
        for user in users:
            if username == user['username'] and check_password_hash(user['password'], password):
                return {
                    'status' : 200,
                    'id' : user['id'],
                    'username' : username,
                    'admin' : user['admin']               
                }, 200

class Meal(Resource):
    """
    The meal resource for the API
    """
    def post(self):
        """
        The post method for creating meals POST api/v1/meals
        """
        name = request.json['name']
        description = request.json['description']

        # Check empty input
        if not name or not description:
            return {
                'status' : 400,
                'message' : 'All fields required!'
            }, 400

        # Check for empty strings
        elif len(name.split()) == 0 or len(description.split()) == 0:
            return {
                'status' : 400,
                'message' : 'Invalid input!'
            }, 400

        # Buffer double entry
        else:
            for meal in meals:
                if name == meal['name']:
                    return {
                        'status' : 409,
                        'message' : 'Meal already exists!'
                    }, 409

        # Instantiate menu object
        new_meal = MealOption(name=name,
                              description=description,
                              owner=User._ID)

        # Store user object
        new_meal_holder = {}
        new_meal_holder['id'] = new_meal._ID
        new_meal_holder['name'] = name
        new_meal_holder['description'] = description
        new_meal_holder['owner'] = User._ID

        meals.append(new_meal_holder)

        return {
            'status' : 201,
            'id' : new_meal._ID,
            'name' : name,
            'description' : description,
            'owner' : new_meal.owner
        }, 201


    def get(self):
        """
        The get method for retrieving meals GET api/v1/meals
        """ 
        # Check if meAls exist
        if len(meals) == 0:
            return {
                'status' : 404,
                'message' : 'No results found!'
            }, 404
        else:   
            return {
                'status' : 200,
                'num_of_meals' : len(meals),
                'meals' : meals
            }, 200

class SingleMeal(Resource):
    """
    The individual meal resource for the API
    """
    def get(self, id):
        """
        The get method for retrieving a single meal GET api/v1/meals/<int:id>
        """
        # Match the meak by id then return
        for meal in meals:        
            if int(meal['id']) == id:
                return {
                    'status' : 200,
                    'id' : meal['id'],
                    'name' : meal['name'],
                    'description' : meal['description']
                }, 200
            else:
                return {
                    'status' : 404,
                    'message' : 'Meal does not exist!'
                }, 404

    def put(self, id):
        """
        The put method for updating a meal PUT api/v1/meals/<int:id>
        """ 
        description = request.json['description']
        
        # Check empty input
        if not description:
            return {
                'status': 400,
                'message' : 'Description can\'t be null!'
            },400

        # Check for empty string values
        elif len(description.split()) == 0:
            return {
                'status' : 400,
                'message' : 'Invalid input!'
            }, 400
        
        if description:
            for meal in meals:
                if int(meal['id']) == id:
                    meal['description'] = description
                    return {
                        'status' : 200,
                        'message' : 'Updated!',
                        'meal' : meal
                    }, 200

    def delete(self, id):
        """
        The delete method for removing a meal option DELETE api/v1/meals/<int:id>
        """

        # Check if meals exist
        if len(meals) == 0:
            return {
                'status' : 404,
                'message' : 'No meals exist'
            }, 404
        
        # Select meal by id and delete it
        for meal in meals:
            if int(meal['id']) == id:
                del meals[meal['id']]
                return {
                    'status' : 200,
                    'message' : 'Meal deleted!'
                }, 200
            
            # Check if the meal exists 
            elif id not in [meal['id'] for meal in meals]:
                return {
                    'status' : 404,
                    'message' : 'Meal does not exist!'
                }, 404

class Menu(Resource):
    """
    The menu resource for the API
    """
    def post(self):
        """
        The method to create a menu POST api/v1/menu
        """
        day = request.json['day']
        menu_meals = request.json['meals']

        # Check for empty entries
        if not day and not menu_meals:
            return {
                'status' : 400,
                'message' : 'All fields are required!'
            }, 400
        
        # Check for empty strings
        elif len(day.split()) == 0 or len(menu_meals) == 0:
            return {
                'status' : 400,
                'message' : 'Invalid input!'
            }, 400

        meals_to_commit=[]

        # Check if selected meals exist, if so add to menu 
        for menu_meal in menu_meals:
            if menu_meal in [meal['name'] for meal in meals]:
                for meal in meals:
                    if meal['name'] == menu_meal:
                        meals_to_commit.append(meal)
           
                        
        # Instantiate menu object
        new_menu = MenuObj(day=day,
                           meals=meals_to_commit,
                           owner=User._ID)

        # Store menu 
        new_menu_holder = {}
        new_menu_holder['id'] = new_menu._ID
        new_menu_holder['day'] = day,
        new_menu_holder['meals'] = meals_to_commit,
        new_menu_holder['owner'] = User._ID
      
        if new_menu: 
            for menu in menus:
                if menu['day'] == new_menu_holder['day']:
                    return {
                            'status' : 409,
                            'message' : 'Menu for ' + str(new_menu_holder['day']) + 'is already set!'
                            }, 409         
            menus.append(new_menu_holder)            
        else:
            return jsonify({
                'message' : 'Menu not created!'
            })       
        

        return {
            'status' : 200,
            'id' : new_menu._ID,
            'day' : day,
            'meals' : meals_to_commit
        }, 200
                   
                    







      