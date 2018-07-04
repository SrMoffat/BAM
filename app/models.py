from werkzeug.security import generate_password_hash, check_password_hash

class User(object):
    """
    The model class for the users
    """
    

    def __init__(self, username, password, admin):
        """
        Constructor for the user class
        """
        _ID = 1
        self.id = User._ID
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.admin = False

        User._ID += 1

    def check_if_admin(self):
        """
        Return True if user is Admin
        """
        return self.admin
    
    def verify_password(self, password):
        """
        Check if the hash values of the password matches that in storage
        :return True if they match
        """
        return check_password_hash(self.password_hash, password)

    def user_info(self):
        """
        Return the user credentials and details
        """
        user_holder = {
            'id' : self._ID,
            'username' : self.username,            
            'admin' : self.email
        }
        return user_holder

class MealOption(object):
    """
    The model class for the meals
    """
    _ID = 1

    def __init__(self, name, description, owner):
        """
        Constructor for the meal class
        """
        self.id = MealOption._ID
        self.name = name
        self.description = description
        self.owner = User._ID

        MealOption._ID += 1

    def get_meal_owner(self, meal_id):
        """
        Return the user associated with a meal
        """
        for meal in meals:
            if meal['id'] == meal_id:
                return meal['owner']

    def meal_holder(self):
        """
        Get the meal and its details
        """
        meal_details = {
            'id' : self._ID,
            'name' : self.name,
            'description' : self.description,
            'owner' : self.owner
        }
        return meal_details
    
class Menu(object):
    """
    The model class for the menu
    """
    _ID = 1
    def __init__(self,day,meals,owner):
        """
        The constructor method for the menu
        """
        self.id = Menu._ID        
        self.day = day
        self.meals = []
        self.owner = User._ID

        Menu._ID += 1

    def get_menu_by_owner(self, menu_id):
        """
        Get the menu by owner
        """
        for menu in menus:
            if menu['id'] == menu_id:
                return menu['owner']
