from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

db = SQLAlchemy()
def init_db(app):
    db.init_app(app) 