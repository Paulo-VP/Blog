from db import db
from sqlalchemy.orm import Mapped, mapped_column
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from typing import List
from datetime import datetime, timedelta
import enum

bcrypt=Bcrypt()

class Users(db.Model,UserMixin):
    __tablename__='users' 
    id:Mapped[int]=mapped_column(primary_key=True, autoincrement=True)
    #nickname:Mapped[str]=mapped_column(nullable=False,unique=True)
    profile_image:Mapped[str]=mapped_column(db.String(255), nullable=False)
    first_name:Mapped[str]=mapped_column(db.String(20), nullable=False)
    last_name:Mapped[str]=mapped_column(db.String(20), nullable=False)
    correo:Mapped[str]=mapped_column(db.String(50), nullable=False,unique=True)
    password:Mapped[str]=mapped_column(db.String(80), nullable=False)


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
            profile_image="default.png",
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
    
    @classmethod
    def getPublicInfoById(cls,id):
        public_info=db.session.execute(db.select(cls.first_name,cls.last_name,cls.correo,cls.profile_image).where(cls.id == id)).mappings().fetchone()
        return public_info
        
class Tokens_create_account(db.Model):
    __tablename__='tokens_create_account' 
    id:Mapped[int]=mapped_column(primary_key=True, autoincrement=True)
    correo:Mapped[str]=mapped_column(db.String(50), nullable=False,unique=True)
    token:Mapped[str]=mapped_column(db.String(255), nullable=False)
    created_at:Mapped[datetime] = mapped_column(nullable=False)
    expires_at:Mapped[datetime] = mapped_column(nullable=False)
    
    def __repr__(self):
        return f'{self.correo} {self.token}'
    
    @classmethod
    def add_token(cls,correo,token):
        new_token=cls(
            correo=correo,
            token=token,
            created_at=datetime.utcnow().isoformat(),
            expires_at=(datetime.utcnow() + timedelta(hours=24)).isoformat()
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
    user_correo:Mapped[str]=mapped_column(db.String(50), nullable=False,unique=True)
    token:Mapped[str]=mapped_column(db.String(255), nullable=False)
    created_at:Mapped[datetime] = mapped_column(nullable=False)
    expires_at:Mapped[datetime] = mapped_column(nullable=False)

    @classmethod
    def add_token(cls,correo,token):
        new_token=cls(
            user_correo=correo,
            token=token,
            created_at=datetime.utcnow().isoformat(),
            expires_at=(datetime.utcnow() + timedelta(hours=24)).isoformat()
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

class PostStatus(enum.Enum):
    public = "public"
    private = "private"
    disabled = "disabled"

class Post(db.Model):
    __tablename__='post' 
    id:Mapped[int]=mapped_column(primary_key=True, autoincrement=True)
    title:Mapped[str]=mapped_column(db.String(80),nullable=False)
    text_color:Mapped[str]=mapped_column(db.String(18),nullable=False)
    card_color:Mapped[str]=mapped_column(db.String(18),nullable=False)
    slug:Mapped[str]=mapped_column(db.String(255),nullable=False, unique=True)
    content:Mapped[str]=mapped_column(db.Text)
    created_at:Mapped[datetime]=mapped_column(nullable=False)
    updated_at:Mapped[datetime]=mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(db.Enum(PostStatus),nullable=False)
    users_id:Mapped[int]=mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f"<Post id={self.id} title={self.title} title={self.slug}>"

    @classmethod
    def createPost(cls,title,text_color,card_color,slug,status,users_id):
        new_post=cls(
            title=title,
            text_color=text_color,
            card_color=card_color,
            slug=slug,
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat(),
            status=PostStatus.public,
            users_id=users_id
        )
        try:
            db.session.add(new_post)
        except:
            db.session.rollback()
            return False
        finally:
            db.session.commit()
            return new_post

    def addContent(self,content):
        try:
            self.content=content
            db.session.commit()
            return True
        except:
            return False
    
    @classmethod
    def existBySlug(cls,slug):
        if(db.session.execute(db.select(cls).where(cls.slug == slug)).scalar()):
            return True
        else:
            return False
        
    @classmethod
    def getAll(cls):
        posts_info=db.session.execute(db.select(cls.title,cls.text_color,cls.card_color,cls.slug,cls.updated_at,cls.users_id,Users.first_name,Users.last_name,Users.profile_image).join(Users,cls.users_id==Users.id)).mappings()
        if(posts_info):
            return posts_info
        else:
            return False
    
    @classmethod
    def getAllById(cls,users_id):
        posts_info=db.session.execute(db.select(cls.title,cls.text_color,cls.card_color,cls.slug,cls.updated_at,cls.users_id,Users.first_name,Users.last_name,Users.profile_image).join(Users,cls.users_id==Users.id).where(cls.users_id == users_id)).mappings()
        if(posts_info):
            return posts_info
        else:
            return False
        
    @classmethod
    def getBySlug(cls,slug_request):
        slug=db.session.execute(db.select(cls).where(cls.slug == slug_request)).scalar()
        if(slug):
            return slug
        else:
            return False
        
class Comments(db.Model):
    __tablename__= 'comments'
    id:Mapped[int]=mapped_column(primary_key=True, autoincrement=True)
    content:Mapped[str]=mapped_column(db.String(300),nullable=False)
    created_at:Mapped[datetime]=mapped_column(nullable=False)
    is_public:Mapped[bool]=mapped_column(db.Boolean, nullable=False)
    users_id:Mapped[int]=mapped_column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id:Mapped[int]=mapped_column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    parent_comment_id:Mapped[int]=mapped_column(db.Integer, db.ForeignKey('comments.id'))

    def __repr__(self):
        return f"<Post id={self.id} content={self.content} post_id={self.post_id} create_at={self.created_at}>"

    @classmethod
    def add_comment(cls,content,is_public,users_id,post_id,parent_comment_id):
        new_comment=cls(
            content=content,
            created_at=datetime.utcnow().isoformat(),
            is_public=is_public,
            users_id=users_id,
            post_id=post_id,
            parent_comment_id=parent_comment_id
        )
        try:
            db.session.add(new_comment)
        except:
            db.session.rollback()
            return False
        finally:
            db.session.commit()
            return new_comment
        
    @classmethod
    def get_comments_post(cls,post_id):
        comments=db.session.execute(db.select(cls.content,cls.created_at,Users.first_name,Users.last_name,Users.profile_image).where(cls.post_id == post_id).join(Users,cls.users_id==Users.id)).mappings()
        if(comments):
            return comments
        else:
            return False

"""
class Followers(db.Model):
    __tablename__='followers'
    id: Mapped[int]=mapped_column(primary_key=True, autoincrement=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("User.id")),
    follower_id:Mapped[int]=mapped_column(ForeignKey("User.id"))
"""