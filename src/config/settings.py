import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret')  # JWT için gizli anahtar
    # MySQL bağlantı bilgisi
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 
        'mysql+pymysql://aquai:aquai123!!@4.233.145.179:3306/aquai'
    )  # MySQL URI formatı
    # SQLAlchemy ayarları
    SQLALCHEMY_TRACK_MODIFICATIONS = False
     # Debug modu
    DEBUG = True
    