import os

EV_SECRET_KEY = os.getenv('SECRET_KEY')  
DB_HOST = os.getenv('DB_HOST') 
DB_USER = os.getenv('MYSQL_USER')
DB_PASSWORD = os.getenv('MYSQL_PASSWORD')  
DB_NAME = os.getenv('MYSQL_DATABASE')  


class Config:
    SECRET_KEY = EV_SECRET_KEY
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://'+DB_USER+':'+DB_PASSWORD+'@'+DB_HOST+'/'+DB_NAME  
    SQLALCHEMY_TRACK_MODIFICATIONS = False