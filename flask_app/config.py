from os import getenv

class Config():
    SQLALCHEMY_DATABASE_URI = getenv('PSQL_URL','postgresql://localhost:5432/shivamk')
    SECRET_KEY = getenv('SECRET_KEY', 'test_key')
