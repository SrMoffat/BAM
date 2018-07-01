import os 

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """
    The parent configuration class for the API
    """
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = '4fr0c0d3th1ng5' #SECRET = os.environ.get('SECRET')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    """
    The configuration class for the testing environment
    """
    TESTING = True
    DEBUG = True

class DevelopmentConfig(Config):
    """
    The configuration class for the development environment
    """
    DEBUG = True

class StatingConfig(object):
    """
    The configuration class for the stating environment 
    """
    DEBUG = True

class DeploymentConfig(Config):
    """
    The configuration class for the production servers
    """
    DEBUG = False
    TESTING = False

app_config = {
    'testing' : TestingConfig,
    'development' : DevelopmentConfig,
    'staging' : StatingConfig,
    'production' : DeploymentConfig
}
