from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from itsdangerous.url_safe import URLSafeSerializer
from slugify import slugify
from bs4 import BeautifulSoup
from config import Config
from db import init_db
from models import Users,Tokens_create_account,Tokens_password,Post, Comments
import base64
import uuid
import os
import re
import shutil


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

@app.context_processor
def inject_user():
    if not request.endpoint in ['login','create','recovery','logout']:
        return dict(
            id=current_user.id,
            first_name=current_user.first_name,
            last_name=current_user.last_name,
            profile_image=current_user.profile_image
        )
    return {}

@app.route("/create", methods=['GET', 'POST'])
def create():
    token = Tokens_create_account.get(request.args.get("token"))
    if token:
        if request.method=='POST':
            data = request.json
            first_name=data.get("first_name")
            last_name=data.get("last_name")
            correo=token.correo
            password=data.get("password")
            password2=data.get("password2")
            if(first_name and last_name and correo):
                if (re.search(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*()_,.?:<>]).+$", password) and len(password)>=8):
                    if(password==password2):
                        usuario=Users.create(first_name,last_name,correo,password)
                        if(usuario):
                            login_user(usuario)
                            token.delete()
                            return jsonify({'status':'success','message':'Cuenta creada'}), 200
                        return jsonify({'status':'error','message':'Error en la creacion de cuenta'}), 400
                    return jsonify({'status':'error','message':'Las contraseñas deben coincidir'}), 400
                return jsonify({'status':'error','message':'La contraseña no cumple con los parametros'}), 400
            return jsonify({'status':'error','message': 'Faltan Campos'}), 400
        if request.method=='GET':
            return render_template("create-account.html")
    return(redirect(url_for("login")))

@app.route("/login", methods=['GET','POST'])
def login():
    url_token=""
    if request.method=='POST':
        data = request.json
        if(data.get('action')=="login"):
            correo=data.get("correo")
            password=data.get("password")
            usuario=Users.login(correo,password)
            if(usuario):
                login_user(usuario)
                return jsonify({'status':'success','message':'Login'})
            return jsonify({'status':'error','message':'Credenciales erroneas'}), 400
        elif(data.get('action')=="recovery"):
            user = Users.get_by_correo(data.get("correo"))
            if(user):
                token_data = {"uuid": uuid.uuid4().hex}
                token=s_password.dumps(token_data)
                Tokens_password.add_token(user.correo,token)
                url_token="/recovery?token="+token
        elif(data.get('action')=="create"):
            if(not Users.get_by_correo(data.get("correo"))):
                token_data = {"uuid": uuid.uuid4().hex}
                token=s_create.dumps(token_data)
                Tokens_create_account.add_token(data.get("correo"),token)
                url_token="/create?token="+token
        return jsonify({'status':'success','message':'Token enviado','token':url_token})
    return render_template("login.html")

@app.route("/recovery", methods=['GET', 'POST'])
def recovery_password():
    token = Tokens_password.get(request.args.get("token"))
    if token:
        if request.method=='POST':
            data=request.json
            password=data.get("password")
            password2=data.get("password2")
            if (re.search(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*()_,.?:<>]).+$", password) and len(password)>=8):
                if(password==password2):
                    usuario=Users.get_by_correo(token.user_correo)
                    if(usuario):
                        token.delete()
                        usuario.update_password(password)
                        return jsonify({'status':'success','message':'Contraseña cambiada'}), 200
                    return jsonify({'status':'error','message':'Error en el cambio de contraseña'}), 400
                return jsonify({'status':'error','message':'Las contraseñas deben coincidir'}), 400
            return jsonify({'status':'error','message':'La contraseña no cumple con los parametros'}), 400
        return render_template("recovery.html")
    return(redirect(url_for("login")))

@app.route("/")
@login_required
def home():
    posts_info=Post.getAll()
    return render_template("home.html",posts_info=posts_info)

@app.route("/profile",methods=['GET'])
@login_required
def profile():
    id=request.args.get("id")
    if(id):
        user_info=Users.getPublicInfoById(id)
        if(user_info):
            user_info_first_name=user_info.first_name
            user_info_last_name=user_info.last_name
            user_info_correo=user_info.correo
            user_info_profile_image=user_info.profile_image
            posts_info=Post.getAllById(id)
            return render_template("profile.html",user_info_first_name=user_info_first_name,user_info_last_name=user_info_last_name,user_info_correo=user_info_correo,user_info_profile_image=user_info_profile_image,posts_info=posts_info)
    return redirect(url_for("home"))

@app.route("/profile/setting", methods=['GET','POST'])
def profile_setting():
    if(request.method=='POST'):
        data = request.json
        if(data.get("action")=="setImage"):
            image_base64=data.get("image")
            if image_base64:
                header, encoded = image_base64.split(',', 1)
                file_type = header.split('/')[1].split(';')[0]
                image_data = base64.b64decode(encoded)
                filename = f"{uuid.uuid4().hex}.{file_type}"
                filepath = os.path.join(app.root_path+"/static/uploads/profile_image", filename)
                with open(filepath, 'wb') as f:
                    f.write(image_data)
                old_filepath = current_user.profile_image
                if current_user.update("profile_image",filename):
                    if (old_filepath != "default.png"):
                        os.remove(os.path.join(app.root_path+"/static/uploads/profile_image", old_filepath))
                    return jsonify({'status':'success','message': 'Imagen guardada'}),200
                return jsonify({'status':'error','message': 'No se pudo cambiar la imagen'}),400
            return jsonify({'status':'error','message': 'Se debe subir una imagen'}),400
        elif(data.get("action")=="setName"):
            first_name=data.get("first_name") 
            last_name=data.get("last_name") 
            if(first_name or last_name):
                if(first_name and first_name!=current_user.first_name):
                    if(current_user.update("first_name",first_name)):
                        return jsonify({'status':'success','message': 'Nombre cambiado'}),200
                    return jsonify({'status':'error','message': 'No se pudo cambiar el nombre'}),400  
                if(last_name and last_name!=current_user.first_name):
                    if(current_user.update("first_name",first_name)):
                        return jsonify({'status':'success','message': 'Nombre cambiado'}),200
                    return jsonify({'status':'error','message': 'No se pudo cambiar el apellido'}),400  
                return jsonify({'status':'error','message': 'No se introdujo informacion nueva'}),400  
            return jsonify({'status':'error','message': 'No se ha enviado datos'}),400                    
        elif(data.get("action")=="correo"):
            correo=request.form.get("correo") 
            current_user.update("correo",correo)
        elif(data.get("action")=="setPassword"):
            old_password=data.get("old_password") 
            new_password=data.get("password") 
            new_password2=data.get("password2") 
            if old_password and new_password and new_password2:
                if (re.search(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*()_,.?:<>]).+$", new_password) and len(new_password)>=8):
                    if new_password == new_password2:
                        if current_user.check_password(old_password):
                            current_user.update_password(new_password)
                            return jsonify({'status':'success','message': 'Clave actualizada'}),200
                        return jsonify({'status':'error','message': 'Clave erronea'}),400  
                    return jsonify({'status':'error','message': 'Las claves nuevas no coinciden'}),400  
                return jsonify({'status':'error','message': 'Clave no cumple con los parametros'}),400
            return jsonify({'status':'error','message': 'faltan datos'}),400
    first_name=current_user.first_name
    last_name=current_user.last_name
    profile_image=current_user.profile_image
    correo=current_user.correo
    return render_template("profile-setting.html",first_name=first_name,last_name=last_name,profile_image=profile_image,correo=correo)

@app.route('/post', methods=['GET','POST'])
@login_required
def post():
    slug_request=request.args.get("slug")
    if(slug_request):
        slug=Post.getBySlug(slug_request)
        if(request.method=='POST'):
            data=request.json
            content=data.get("comment")
            is_public=data.get("is_public").lower() == 'true'
            users_id=current_user.id
            post_id=slug.id
            parent_comment_id=data.get("parent_comment")
            if(Comments.add_comment(content,is_public,users_id,post_id,parent_comment_id)):
                return jsonify({'status':'success','message': 'Comentario guardado'}),200
            return jsonify({'status':'error','message': 'No se pudo enviar el comentario'}),400
        info_users=Users.get_by_id(slug.users_id)
        comments=Comments.get_comments_post(slug.id)
        if(Post):
            return render_template("post.html",slug=slug,info_users=info_users,comments=comments)
    return redirect(url_for("home"))

@app.route('/post/create', methods=['POST','GET'])
@login_required
def createPost():
    if(request.method=='POST'):
        data = request.get_json()
        title = data.get('title')
        text_color = data.get('text_color')
        card_color = data.get('card_color')
        slug=slugify(title+"-"+current_user.first_name+"-"+current_user.last_name)
        id_user=current_user.id
        editor_content = data.get('editor_content')
        if(not (title and editor_content)):
            return jsonify({'status': 'error', 'message': 'Faltan datos'}), 400
        if(Post.existBySlug(slug)):
            return jsonify({'status': 'error', 'message': 'Ya has ocupado este titulo en otro Post'}), 400
        new_post=Post.createPost(title,text_color,card_color,slug,"cambiar_por_status",id_user)
        if(new_post):
            soup = BeautifulSoup(editor_content, 'html.parser')
            images = soup.find_all('img')
            path=f"{app.root_path}/static/uploads/{current_user.id}/{slugify(title)}"
            if not os.path.isdir(path):
                os.makedirs(path)
            for img in images:
                src = img.get('src')
                if src.startswith('data:image/'):
                    header, encoded = src.split(',', 1)
                    file_type = header.split('/')[1].split(';')[0]
                    image_data = base64.b64decode(encoded)
                    filename = f"{uuid.uuid4().hex}.{file_type.lower()}"
                    filepath = os.path.join(path,filename)
                    with open(filepath, 'wb') as f:
                        f.write(image_data)
                img['src'] = path=f"/static/uploads/{current_user.id}/{slugify(title)}/{filename}"
            updated_editor_content = str(soup)
            if(new_post.addContent(updated_editor_content)):
                return jsonify({'status': 'success', 'message': 'Post creado'}), 200
        return jsonify({'status': 'error', 'message': 'Error creacion de Post'}), 400
    return render_template("create-post.html")

@app.route('/prueba')
@login_required
def prueba():
    return render_template("prueba.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",port=8080)