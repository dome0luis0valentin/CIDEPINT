from flask import Blueprint
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask import request
from flask import abort
from flask import session
import random
import string

from src.core import auth
from src.web.helpers.auth import is_authenticated
from src.web.helpers.auth import is_valid_confirmation_token

from src.core.models import ConfirmationUser
from src.core.models import User
from flask_mail import Message

from src.core.models import create_confirmation
from src.core.auth import create_user

from authlib.integrations.flask_client import OAuth
from src.core.config.database import db
from flask import current_app

import os
from dotnet import load_dotenv
load_dotenv()

# Código para generar un token de confirmación
def generate_confirmation_token():
    token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
    return token


auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_blueprint.get("/")
def login():
    if not is_authenticated(session):
        return render_template("auth/login.html")
    return redirect("/")


@auth_blueprint.post("/authenticate")
def authenticate():
    params = request.form

    user = auth.check_user(params["email"], params["password"])

    #print("Este es el estado de la sesion", is_authenticated(session))

    if not user:
        #print("Usuario incorrecto")
        flash("Email o clave incorrecta.", "error")
        return redirect(url_for("auth.login"))
    #print("Usuario correcto")

    flash("Bienvenido nuevamente.", "succes")

    session['user'] = user
    session['user_id'] = user.id

    #print(f'Este es el valor : {session.get("user_id")} y este es el otro: {session.get("user").email}')
    return redirect(url_for("home"))


@auth_blueprint.get("/logout")
def logout():
    if session.get("user"):
        del session["user"]
        session.clear()
        flash("La sesión se cerró correctamente.", "info")

    else:
        
        flash("Men, primero tenes que iniciar sesión.", "info")

    return redirect("/")



@auth_blueprint.get("/register")
def register():
    return render_template("auth/register.html")


@auth_blueprint.post("/validate_register")
def validate_register():

    """
    Esta función se encarga de validar el mail y enviarle un mensaje con la URL y token único
    para que termine el registro
    """
    from app import mail
    params = request.form

    email = params["email"]

    user = auth.find_user_by_email_and_pass(email)
    confir = auth.find_confirmation_by_email(email)
    
    if user != None or confir != None:
        #Usuario ya existe
        flash("Lo sentimos, este correo electrónico ya esta registrado. Por Favor si ya te has registrado ve a login", "error")
        return redirect(url_for("auth.register"))

    #Usuario correcto

    # Genera un token de confirmación
    token = generate_confirmation_token()

    confir = create_confirmation(email = email, token = token)

    # Envía el correo electrónico con el token
    msg = Message('Completa tu registro', sender='valentindome777@gmail.com', recipients=[email])
    msg.body = f'¡Hola {email}!\n\nHaz clic en el siguiente enlace para completar tu registro\n\n{url_for("auth.complete_registration", token=token, _external=True)}'
    mail.send(msg)


    flash("Primera etapa exitosa, ahora revisa tu correo electrónico para continuar.", "success")

    # Redirige al usuario a la página principal
    return redirect("/")

@auth_blueprint.route("/complete_registration/<token>", methods=["GET", "POST"])
def complete_registration(token):

    """
    Esta función solo puede ser accedida si previamente se inicio el registro y permite terminar de
    cargar los datos del usuario
    """

    # Verifica si el token es válido
    if is_valid_confirmation_token(token):
        if request.method == "POST":
            # Recupera los datos del formulario de registro (nombre de usuario, contraseña, etc.)
            email = request.form.get("email")
            password = request.form.get("password")
            name = request.form.get("name")
            last_name = request.form.get("last_name")

            # Guarda la información de usuario en la base de datos y asigna el rol correspondiente
            user = create_user(email=email, password=password, name=name, last_name=last_name)
            
            flash("Registro completado. Ahora puedes iniciar sesión.", "success")
            return redirect(url_for("auth.login"))
        else:
            return render_template("auth/complete_registration.html", token=token)
    else:
        flash("El enlace de confirmación es inválido o ha expirado.", "error")
        return redirect(url_for("auth.register"))




'''Configurar la integración de OAuth con Google para la autenticación de usuarios'''

app = current_app
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth(app)
oauth.register(
    name='google',
    redirect_uri='https://admin-grupo24.proyecto2023.linti.unlp.edu.ar/auth/callback',
    client_secret = os.getenv('CLIENT_SECRET')
    client_id = os.getenv('CLIENT_ID')
    # client_secret='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',
    # client_id = '193229960820-ruljkn9bnh3rjftm5b0a0q9840rrtp9v.apps.googleusercontent.com',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    },
    prompt= 'consent'
)


@auth_blueprint.route('/register_google')
def register_google():
    return oauth.google.authorize_redirect('https://admin-grupo24.proyecto2023.linti.unlp.edu.ar/auth/callback')

    # redirect_uri = url_for('callback', _external=True)


@auth_blueprint.route('/callback')
def callback():
    from app import mail
    token = oauth.google.authorize_access_token()
    token_user = (token,'')
    info=token_user[0]
    datos=info['userinfo']
    email=datos['email']
    datosDB = User.query.filter_by(email=email).first()
    #passw = datos['family_name'] +'.'+datos['given_name']
    passw = '123'
    if not datosDB:
        
        # Carga el usuario en la DB
        user=auth.create_user(email= email, password = passw, name=datos['given_name'], last_name=datos['family_name'])
        user.active=True
        db.session.add(user)
        db.session.commit()
        # Envía el correo electrónico con la contraseña
        # msg = Message('Contraseña CIDEPINT', sender='valentindome777@gmail.com', recipients=[email])
        # msg.body = f'¡Hola {email}!\n\nHaz clic en el siguiente enlace para ingresar a nuestra web por primera vez https://grupo24.proyecto2023.linti.unlp.edu.ar/LoginGoogle, su contraseña es {passw}'
        # mail.send(msg)
        flash("Ha sido registrado. Su password es: 123", "success")                
    return redirect('https://grupo24.proyecto2023.linti.unlp.edu.ar/LoginGoogle')



# @auth_blueprint.route('/logout')
# def logout():
#     ''' Revocar el token de acceso al cerrar sesión '''
#     if 'google_token' in session:
#         oauth.google.post(
#             'https://accounts.google.com/o/oauth2/revoke',
#             params={'token': session['google_token']},
#             headers={'Content-Type': 'application/x-www-form-urlencoded'}
#         )
#     session.pop('user', None)
#     session.clear()
#     return redirect('/')   
