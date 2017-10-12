import datetime
# Turns on debugging features in Flask
DEBUG = True
#
# For use in web_app emails
MAIL_FROM_EMAIL = "info@example.com "
#
# This is a secret key that is used by Flask to sign cookies.
# Its also used by extensions like Flask-Bcrypt. You should
# define this in your instance folder to keep it out of version
# control.
SECRET_KEY = 'change_this_please'  # Change for production
#
# Configuration for the Flask-Bcrypt extension
BCRYPT_LEVEL = 12
# ----------------------------------------------------------------
# SLACK CONFIG
# ----------------------------------------------------------------
SLACK_WEBHOOK = " https://hooks.slack.com/services/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 "
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
MONGODB_DB = 'battleship'
MONGODB_HOST = 'localhost'
#
# ----------------------------------------------------------------
# REDIS CONFIGURATIONS
# ----------------------------------------------------------------
#
REDIS_URL = "redis://localhost:6379/0"
