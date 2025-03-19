import jwt
import secrets
from config.settings import Config 
from models.user_model import ApiKey, db, User
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

# bcrypt nesnesini başlatıyoruz (şifreleri güvenli bir şekilde hash'lemek için)
bcrypt = Bcrypt()

def register_user(username, password, email=None, name=None, surname=None):
    # Kullanıcının şifresini hashliyoruz (daha güvenli bir şekilde saklamak için)
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Kullanıcı oluştur
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        raise ValueError("Bu kullanıcı adı zaten alındı.")
    user = User(username=username, password=hashed_password, email=email, name=name, surname=surname)
    db.session.add(user)
    db.session.commit()
    return {"message": f"Kullanıcı {username} başarıyla oluşturuldu!"}

def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        # Şifre doğruysa, JWT token'ı oluşturuyoruz
        access_token = create_access_token(identity=f"{user.id}", expires_delta=timedelta(hours=1))
        refresh_token = create_access_token(identity=f"{user.id}", expires_delta=timedelta(days=30))
        return {"access_token": access_token, "refresh_token": refresh_token}
    return {"error": "Geçersiz kullanıcı adı veya şifre."}

def generate_reset_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1)  # Token 1 saat geçerli
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

def verify_reset_token(token):
    try:
        decoded = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return decoded["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def update_password(user_id, new_password):
    user = User.query.get(user_id)
    if not user:
        return False
    hashed_password = generate_password_hash(new_password)
    user.password = hashed_password
    user.save()  # ORM'ye bağlı olarak değişebilir
    return True

def generate_api_key(user_id, expiration_time_in_days=30):
    """API key oluşturma"""
    api_key = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(days=expiration_time_in_days)
    user = User.query.get(user_id)
    if user:
        new_api_key = ApiKey(api_key=api_key, user_id=user.id, expires_at=expires_at)
        db.session.add(new_api_key)
        db.session.commit()
        return api_key
    return None

def delete_api_key(api_key_id):
    """API key silme"""
    api_key = ApiKey.query.get(api_key_id)
    if api_key:
        db.session.delete(api_key)
        db.session.commit()
        return True
    return False