from db import db
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy import ForeignKey
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from typing import List
import datetime

bcrypt=Bcrypt()

class Users(db.Model,UserMixin):
    __tablename__='users' 
    id:Mapped[int]=mapped_column(primary_key=True, autoincrement=True)
    #nickname:Mapped[str]=mapped_column(nullable=False,unique=True)
    profile_image:Mapped[str]=mapped_column(nullable=False)
    first_name:Mapped[str]=mapped_column(nullable=False)
    last_name:Mapped[str]=mapped_column(nullable=False)
    correo:Mapped[str]=mapped_column(nullable=False,unique=True)
    password:Mapped[str]=mapped_column(nullable=False)


    def __repr__(self):
        return f'{self.id} {self.first_name} {self.last_name} {self.correo}'

    @classmethod
    def login(cls,correo,password):
        user = db.session.execute(db.select(cls).where(cls.correo==correo)).scalar()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                return user 
        return False
    
    @classmethod
    def get_by_correo(cls,correo):
        return db.session.execute(db.select(cls).where(cls.correo == correo)).scalar()

    
    @classmethod
    def create(cls,first_name,last_name,correo,password):
        new_user=cls(
            profile_image="default.jpg",
            first_name=first_name,
            last_name=last_name,
            correo=correo,
            password=bcrypt.generate_password_hash(password).decode('utf-8'),
        )
        try:
            db.session.add(new_user)
        except:
            db.session.rollback()
            return False
        finally:
            db.session.commit()
            return new_user

    @classmethod
    def get_by_id(cls, id):
        return db.session.execute(db.select(cls).where(cls.id == id)).scalar()
    
    def update(self,atribute,new_information):
        setattr(self, atribute, new_information)
        db.session.commit()
        return True

    def check_password(self,password):
        return bcrypt.check_password_hash(self.password, password)
    
    def update_password(self,password):
        self.password=bcrypt.generate_password_hash(password).decode('utf-8')
        db.session.commit()
        return True
        
class Tokens_create_account(db.Model):
    __tablename__='tokens_create_account' 
    id:Mapped[int]=mapped_column(primary_key=True, autoincrement=True)
    correo:Mapped[str]=mapped_column(nullable=False,unique=True)
    token:Mapped[str]=mapped_column(nullable=False)
    created_at:Mapped[datetime.datetime] = mapped_column(nullable=False)
    expires_at:Mapped[datetime.datetime] = mapped_column(nullable=False)
    
    def __repr__(self):
        return f'{self.correo} {self.token}'
    
    @classmethod
    def add_token(cls,correo,token,created_at,expires_at):
        new_token=cls(
            correo=correo,
            token=token,
            created_at=created_at,
            expires_at=expires_at
        )
        old_token=db.session.execute(db.select(cls).where(cls.correo == correo)).scalar()
        if old_token:
            db.session.delete(old_token)
            db.session.commit()
        try:
            db.session.add(new_token)
        except:
            db.session.rollback()
            return False
        finally:
            db.session.commit()
            return True

    @classmethod
    def get(cls,token):
        return db.session.execute(db.select(cls).where(cls.token == token)).scalar()
    
    def delete(sefl):
        db.session.delete(sefl)
        db.session.commit()

class Tokens_password(db.Model):
    __tablename__='tokens_password' 
    id:Mapped[int]=mapped_column(primary_key=True, autoincrement=True)
    user_correo:Mapped[str]=mapped_column(nullable=False,unique=True)
    token:Mapped[str]=mapped_column(nullable=False)
    created_at:Mapped[datetime.datetime] = mapped_column(nullable=False)
    expires_at:Mapped[datetime.datetime] = mapped_column(nullable=False)

    @classmethod
    def add_token(cls,correo,token,created_at,expires_at):
        new_token=cls(
            user_correo=correo,
            token=token,
            created_at=created_at,
            expires_at=expires_at
        )
        old_token=db.session.execute(db.select(cls).where(cls.user_correo == correo)).scalar()
        if old_token:
            db.session.delete(old_token)
            db.session.commit()
        try:
            db.session.add(new_token)
        except:
            db.session.rollback()
            return False
        finally:
            db.session.commit()
            return True
    
    @classmethod
    def get(cls,token):
        return db.session.execute(db.select(cls).where(cls.token == token)).scalar()

    def delete(sefl):
        db.session.delete(sefl)
        db.session.commit()
        
"""
class Followers(db.Model):
    __tablename__='followers'
    id: Mapped[int]=mapped_column(primary_key=True, autoincrement=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("User.id")),
    follower_id:Mapped[int]=mapped_column(ForeignKey("User.id"))
"""