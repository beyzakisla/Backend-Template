Flask Backend API

Bu proje, kullanıcı kayıt ve giriş işlemlerini sağlayan basit bir Flask tabanlı API’dir. API, JWT (JSON Web Token) kullanarak kullanıcı kimlik doğrulaması yapar ve kullanıcı verilerini bir veritabanında saklar.

Özellikler

	•	Kullanıcı kayıt işlemi
	•	Kullanıcı giriş işlemi
	•	JWT tabanlı kimlik doğrulama
	•	Basit veritabanı işlemleri (SQLAlchemy kullanılarak)

Kullanılan Teknolojiler

	•	Python 3
	•	Flask
	•	Flask-JWT-Extended
	•	Flask-SQLAlchemy
	•	Requests (API testleri için)# Backend-Template
 ### **Genel Yapı**

1. **`user_routes.py` (Routes Katmanı)**:
    - Gelen HTTP isteklerini işler.
    - Controller çağrıları yapar.
    - Kullanıcıdan veri alır ve cevabı döner.
2. **`user_controller.py` (Controller Katmanı)**:
    - İş mantığını yönetir.
    - `auth_service` gibi servisleri çağırır.
    - Verileri düzenler ve kontrol eder.
3. **`auth_service.py` (Service Katmanı)**:
    - Veritabanı ve şifreleme işlemlerini yapar.
    - Kullanıcı kayıt ve giriş işlemleri burada olur.
4. **`user_model.py`**:
    - Kullanıcı modelini (veritabanı tablosu) tanımlar.
# Backend-Template
