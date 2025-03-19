# Python 3.10 imajını temel alıyoruz
FROM python:3.10-slim

# Çalışma dizini oluşturuyoruz
WORKDIR /app

# Gereksinimlerin olduğu dosyayı konteynere kopyalıyoruz
COPY requirements.txt /app/

# Python bağımlılıklarını yüklüyoruz
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını konteynere kopyalıyoruz
COPY . /app/

# Flask uygulamasının 5000 numaralı portu dinlemesini sağlıyoruz
EXPOSE 5000

# Flask uygulamasını çalıştırıyoruz
CMD ["python", "src/app.py"]