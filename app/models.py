from werkzeug.security import generate_password_hash, check_password_hash

class User(object):
    """
    The model class for the users
    """
    _ID = 0

    def __init__(self, username, password, admin):
        """
        Constructor for the user class
        """
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
            'email' : self.email,
            'admin' : self.email
        }
        return user_holder
