class Config(object):
    # ... other configuration keys

    # MySQL configurations
    MYSQL_DATABASE_USER = 'your_username'
    MYSQL_DATABASE_PASSWORD = 'your_password'
    MYSQL_DATABASE_DB = 'your_database'
    MYSQL_DATABASE_HOST = 'localhost' # or your database server address
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{MYSQL_DATABASE_USER}:{MYSQL_DATABASE_PASSWORD}@{MYSQL_DATABASE_HOST}/{MYSQL_DATABASE_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False