import os

# class Config:
#     """Base configuration class."""
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'randomized_chart_data.sqlite')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'randomized_chart_data.sqlite')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH

    # Add other general configurations here
class DevelopmentConfig(Config):
    """Development configuration class."""
    DEBUG = True
    # Development-specific configurations

class ProductionConfig(Config):
    """Production configuration class."""
    DEBUG = False
    # Production-specific configurations