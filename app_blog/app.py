from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from itsdangerous.url_safe import URLSafeSerializer
from datetime import datetime, timedelta
from config import Config
from db import init_db
from models import Users,Tokens_create_account,Tokens_password
import uuid
import os

app = Flask(__name__)
app.config.from_object(Config)
init_db(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
s_create=URLSafeSerializer('abcdefg',salt="create")
s_password=URLSafeSerializer('abcdefg',salt="password")


@login_manager.user_loader
def load_user(user_id): 
    return Users.query.get(int(user_id))

@app.route("/create", methods=['GET', 'POST'])
def create():
    token = Tokens_create_account.get(request.args.get("token"))
    if token:
        if request.method=='POST':
            first_name=request.form.get("first_name")
            last_name=request.form.get("last_name")
            correo=token.correo
            password=request.form.get("password")
            password2=request.form.get("password2")
            if(password==password2):
                usuario=Users.create(first_name,last_name,correo,password)
                if(usuario):
                    login_user(usuario)
                    token.delete()
                    return(redirect(url_for("home")))
        return render_template("create.html")
    return(redirect(url_for("login")))

@app.route("/login", methods=['GET','POST'])
def login():
    url_token=""
    if request.method=='POST':
        action=request.form.get("action")
        if(action=="login"):
            correo=request.form.get("correo")
            password=request.form.get("password")
            usuario=Users.login(correo,password)
            if(usuario):
                login_user(usuario)
                return(redirect(url_for("home")))
        elif(action=="recovery"):
            user = Users.get_by_correo(request.form.get("correo"))
            if(user):
                token_data = {"uuid": uuid.uuid4().hex}
                token=s_password.dumps(token_data)
                Tokens_password.add_token(user.correo,token,datetime.utcnow().isoformat(),(datetime.utcnow() + timedelta(hours=24)).isoformat())
                url_token="/recovery?token="+token
        elif(action=="create"):
            if(not Users.get_by_correo(request.form.get("correo"))):
                token_data = {"uuid": uuid.uuid4().hex}
                token=s_create.dumps(token_data)
                Tokens_create_account.add_token(request.form.get("correo"),token,datetime.utcnow().isoformat(),(datetime.utcnow() + timedelta(hours=24)).isoformat())
                url_token="/create?token="+token
    return render_template("login.html",url_token=url_token)

@app.route("/recovery", methods=['GET', 'POST'])
def recovery_password():
    token = Tokens_password.get(request.args.get("token"))
    if token:
        if request.method=='POST':
            password=request.form.get("password")
            password2=request.form.get("password2")
            if(password==password2):
                usuario=Users.get_by_correo(token.user_correo)
                if(usuario):
                    token.delete()
                    usuario.update_password(password)
                    return(redirect(url_for("login")))
        return render_template("recovery.html")
    return(redirect(url_for("login")))

@app.route("/")
@login_required
def home():
    return render_template("home.html", first_name=current_user.first_name, profile_image=current_user.profile_image)

@app.route("/profile")
@login_required
def profile():
    first_name=current_user.first_name
    last_name=current_user.last_name
    correo=current_user.correo
    profile_image=current_user.profile_image
    return render_template("profile.html",first_name=first_name,last_name=last_name,correo=correo,profile_image=profile_image)

@app.route("/profile/setting", methods=['GET','POST'])
def profile_setting():
    if(request.method=='POST'):
        action=request.form.get("action")
        if(action=="profile_image"):
            profile_image=request.files['profile_image']
            if profile_image:
                filename = f"{uuid.uuid4().hex}.{profile_image.filename.rsplit('.', 1)[1].lower()}"
                filepath = os.path.join('/app/static/uploads/profile_image', filename)
                profile_image.save(filepath)
                old_filepath = current_user.profile_image
                if current_user.update("profile_image",filename):
                    if (old_filepath != "default.jpg"):
                        os.remove(os.path.join('/app/static/uploads/profile_image', old_filepath))
        elif(action=="name"):
            first_name=request.form.get("first_name") 
            last_name=request.form.get("last_name") 
            for field, value in request.form.items():
                if hasattr(current_user, field) and value and value != str(getattr(current_user, field)):
                    current_user.update(field,value)
        elif(action=="correo"):
            correo=request.form.get("correo") 
            current_user.update("correo",correo)
        elif(action=="password"):
            old_password=request.form.get("old_password") 
            new_password=request.form.get("new_password") 
            new_password2=request.form.get("new_password2") 
            if old_password and new_password and new_password2:
                if new_password == new_password2:
                    if current_user.check_password(old_password):
                        current_user.update_password(new_password)
    first_name=current_user.first_name
    last_name=current_user.last_name
    profile_image=current_user.profile_image
    correo=current_user.correo
    return render_template("profile_setting.html",first_name=first_name,last_name=last_name,profile_image=profile_image,correo=correo)

@app.route('/post')
@login_required
def post():
    return render_template("post.html")


@app.route('/prueba')
def prueba():
    return render_template("prueba.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=8080)