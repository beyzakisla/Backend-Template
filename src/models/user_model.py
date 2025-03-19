from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users' # Veritabanındaki tablonun adı
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120)) 
    surname = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=db.func.now())

    api_keys = db.relationship('ApiKey', back_populates='user')  # API Key ilişkilendirmesi

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        """JSON yanıtı için dictionary dönüştürücüsü"""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "name": self.name,
            "surname": self.surname,
            "created_at": self.created_at
        }
    
class ApiKey(db.Model):
    __tablename__ = 'api_keys'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    api_key = db.Column(db.String(256), unique=True, nullable=False)  # API key değeri
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used_at = db.Column(db.DateTime, nullable=True)  # İlk kullanım tarihi
    expires_at = db.Column(db.DateTime, nullable=False)  # API key'in süresi

    user = db.relationship('User', back_populates='api_keys')