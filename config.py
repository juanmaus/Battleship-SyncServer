import datetime
# Turns on debugging features in Flask
DEBUG = True
#
# For use in web_app emails
MAIL_FROM_EMAIL = "info@gernet-api.org"
#
# This is a secret key that is used by Flask to sign cookies.
# Its also used by extensions like Flask-Bcrypt. You should
# define this in your instance folder to keep it out of version
# control.
SECRET_KEY = 'change_this_please'  # Change for production
#
# Configuration for the Flask-Bcrypt extension
BCRYPT_LEVEL = 12
#
# ----------------------------------------------------------------
# JWT CONFIGURATIONS
# ----------------------------------------------------------------
JWT_AUTH_URL_RULE = '/api/v1/auth'
JWT_EXPIRATION_DELTA = datetime.timedelta(3200) # Set the token validity
#
# ----------------------------------------------------------------
# MONGO DATABASE CONFIGURATION
# ----------------------------------------------------------------
# MongoDB configuration parameters
MONGODB_DB = 'the_db_name'
MONGODB_HOST = 'mongo_host'
MONGODB_PORT = 57112
MONGODB_USERNAME = 'your_username'
MONGODB_PASSWORD = 'secrete_password_here'
