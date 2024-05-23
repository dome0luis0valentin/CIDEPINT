from flask import jsonify
from flask import Blueprint, url_for, redirect, session
from src.web.helpers.auth import login_required
from src.core.controller.errors import error_401
from flask import request, make_response
from src.core.auth import check_user, find_user_by_id
from src.core.config import database
from src.core.seeds import run
from flask_jwt_extended import create_access_token, jwt_required, unset_jwt_cookies

auth_api_bp = Blueprint("auth_api",__name__,url_prefix="/api/auth/")

@auth_api_bp.post('/')
def login_jwt():
    if request.method == "OPTIONS":
        return make_response()
    data = request.get_json()
    email = data['email']
    password = data[ 'password']
    user = check_user(email, password)
    if user:
        # Si las credenciales son correctas, crea un token de acceso
        access_token = create_access_token(identity=user.id)
        return jsonify(token=access_token), 200
    else:
        return jsonify (message="Unauthorized"), 401

@auth_api_bp.route('/logout_jwt', methods=['GET'])
@jwt_required() 
def logout_jwt():
    response = jsonify(unset_jwt_cookies(response))
    return response, 200

# @auth_api_bp.route('/user_jwt', methods=['GET'])
# @jwt_required()
# def user_jwt ():
#     current_user = get_jwt_identity()
#     user = find_user_by_id(current_user)
#     response = jsonify(user)
#     return response, 200

@auth_api_bp.route("/seeds-db", methods=["POST"])
def seeds():
    try:
        data = request.get_json()
        if not data or ('user' and 'password' not in data) or data["user"] != 'admin' or data["password"] != 'grupo24':
            return {"result": "fail"}, 401
    except:
        return {"result": "fail"}, 401
    run()
    return {"result": "success seeds"}, 200

@auth_api_bp.route("/reset-db", methods=["POST"])
def reset_db():
    try:
        data = request.get_json()
        if not data or ('user' and 'password' not in data) or data["user"] != 'admin' or data["password"] != 'grupo24':
            return {"result": "fail"}, 401
    except:
        return {"result": "fail"}, 401
    database.reset_db()
    return {"result": "success create db"}, 200

@auth_api_bp.route("/reset-seeds-db", methods=["POST"])
def create_seeds_db():
    try:
        data = request.get_json()
        if not data or ('user' and 'password' not in data) or data["user"] != 'admin' or data["password"] != 'grupo24':
            return {"result": "fail"}, 401
    except:
        return {"result": "fail"}, 401
    database.reset_db()
    run()
    return {"result": "success reset db and seeds"}, 200