from flask import Blueprint, request, jsonify
from models.user_model import User, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.auth_service import register_user, login_user, generate_api_key
from controllers.user_controller import UserController

# Blueprint ile kullanıcıyla ilgili işlemleri bir araya getiriyoruz
user_bp = Blueprint('user_bp', __name__)

# Kullanıcı Kayıt Endpoint'i
@user_bp.route('/register', methods=['POST'])
def register_endpoint():
    # İstekten gelen veriyi alıyoruz
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    name = data.get("name")
    surname = data.get("surname")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # UserController üzerinden kullanıcı kaydını gerçekleştiriyoruz
    try:
        result = UserController.register(username, password, email, name, surname)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# Kullanıcı Giriş Endpoint'i
@user_bp.route('/login', methods=['POST'])
def login_endpoint():
    # İstekten gelen veriyi alıyoruz
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # UserController üzerinden kullanıcı girişini doğruluyoruz
    result = UserController.login(username, password)
    
    # Eğer JWT token oluşturulmuşsa, bunu geri döndürüyoruz
    if "access_token" in result:
        return jsonify(result), 200
    return jsonify(result), 401


# Kullanıcıları Listeleme (GET isteği)
@user_bp.route('/', methods=['GET'])
def get_all_users():
    users = User.query.all()  # Tüm kullanıcıları veritabanından al
    user_list = [{"username": user.username} for user in users]
    return jsonify(user_list), 200


# Korunmuş Endpoint (JWT gerektirir)
@user_bp.route('/protected', methods=['GET'])
@jwt_required()  # JWT gerektirir
def protected():
    current_user = get_jwt_identity()  # Token'dan kullanıcıyı al
    return jsonify(logged_in_as=current_user), 200


# Şifre sıfırlama isteği
@user_bp.route('/password-reset', methods=['POST'])
def password_reset_request():
    data = request.json
    email = data.get('email')
    if not email:
        return jsonify({"error": "Email is required"}), 400
    return UserController.request_password_reset(email)

# Şifre sıfırlama
@user_bp.route('/password-reset/<token>', methods=['POST'])
def password_reset(token):
    data = request.json
    new_password = data.get('password')
    if not new_password:
        return jsonify({"error": "Password is required"}), 400
    return UserController.reset_password(token, new_password)

# Kullanıcı API Key Oluşturma
@user_bp.route('/generate_api_key', methods=['POST'])
def create_generate_api_key():
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    
    api_key = generate_api_key(user_id)

    if api_key:
        return jsonify({"api_key": api_key}), 201
    return jsonify({"error": "API key generation failed"}), 400

# Kullanıcı API Key Silme
@user_bp.route('/api-key/<int:api_key_id>', methods=['DELETE'])
def delete_api_key(api_key_id):
    result = UserController.delete_api_key(api_key_id)
    if result:
        return jsonify({"message": "API Key başarıyla silindi."}), 200
    return jsonify({"error": "API Key silinemedi."}), 400