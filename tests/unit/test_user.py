import requests

BASE_URL = "http://127.0.0.1:5000"  # API'nizin adresi

# Kayıt Verisi
register_data = {"username": "testuser", "password": "123456"}

# Kayıt Endpoint'ine POST isteği gönder
response = requests.post(f"{BASE_URL}/api/users/register", json=register_data)

# Yanıtı ham metin olarak kontrol et
print("Kayıt Yanıtı (Ham Metin):", response.text)

# Yanıtın JSON olup olmadığını kontrol et
try:
    print("Kayıt Yanıtı (JSON):", response.json())
except ValueError as e:
    print("JSON hata:", e)

# Kullanıcı Girişi Testi
login_data = {"username": "testuser", "password": "123456"}

# Giriş Endpoint'ine POST isteği gönder
response = requests.post(f"{BASE_URL}/api/users/login", json=login_data)

# Yanıtı ham metin olarak kontrol et
print("Giriş Yanıtı (Ham Metin):", response.text)

try:
    login_response = response.json()
    if "access_token" in login_response:
        print("Giriş başarılı, Token alındı:", login_response["access_token"])
    else:
        print("Giriş başarısız:", login_response.get("error"))
except ValueError as e:
    print("JSON hata:", e)