from flask import Flask, jsonify, request
from flask_cors import CORS
from routes.user_routes import user_bp
from config.settings import Config
from models.user_model import db
from flask_jwt_extended import JWTManager, decode_token, create_access_token, jwt_required, get_jwt_identity
from sqlalchemy import Table

def create_app():
    app = Flask(__name__)
    
    # CORS'u özelleştirerek etkinleştir
    CORS(app, resources={r"/*": {"origins": "https://aquai.tech"}}, supports_credentials=True)

    app.config.from_object(Config)

    # Blueprint'i bağla
    app.register_blueprint(user_bp, url_prefix='/api/users')

    # JWT Manager'i başlat
    jwt = JWTManager(app)

    # Veritabanını başlatmak için db.init_app'ı yalnızca bir kez çağır
    db.init_app(app)

    # Veritabanını oluştur
    with app.app_context():
        db.create_all()

    # Veritabanındaki tabloları listeleyen route
    @app.route('/check_tables', methods=['GET'])
    def check_tables():
        try:
            with app.app_context():
                tables = db.metadata.tables.keys()
                if not tables:
                    return jsonify({"message": "Veritabanında hiç tablo bulunamadı!"}), 404                
                return jsonify({"tables": list(tables)}), 200
        except Exception as e:
            return {"error": str(e)}, 500


    # Belirli bir tablonun içeriğini listeleyen route
    @app.route('/check_table_data/<table_name>', methods=['GET'])
    def check_table_data(table_name):
        try:
            with app.app_context():
            # Tablonun adının doğruluğunu kontrol et
                if table_name not in db.metadata.tables:
                    return jsonify({"error": f"Tablo '{table_name}' bulunamadı."}), 404

            # Tablonun tüm verilerini çek
            table = db.metadata.tables[table_name]
            results = db.session.execute(table.select()).fetchall()

            # Eğer tablo boşsa bilgi döndür
            if not results:
                return jsonify({"message": f"Tablo '{table_name}' boş."}), 200

            # Sütun isimlerini ve satırları JSON formatına çevirir
            columns = table.columns.keys()  # Tablo sütun isimlerini al
            data = [dict(zip(columns, row)) for row in results]  # Sütun isimleri ile verileri eşleştir

            return jsonify({"table": table_name, "columns": columns, "data": data}), 200  # JSON formatında yanıt döndür
        except Exception as e:
            return {"error": str(e)}, 500
        
    @app.route('/jwt/verify', methods=['POST'])
    def verify():
        try:
            if request.content_type is None or "application/json" not in request.content_type:
                return jsonify({"error": "Content-Type must be application/json"}), 400
            if not request.is_json:
                return jsonify({"error": "Invalid JSON"}), 400
            token = request.headers.get('Authorization')
            if token and token.startswith('Bearer '):
                token = token.split(' ')[1]
            if not token:
                return jsonify({"error": "Token is required"}), 400
            decoded = decode_token(token)
            if not decoded:
                return jsonify({"error": "Invalid token"}), 400
            return jsonify({"token": token, "valid": True}), 200
        except Exception as e:
            return {"valid": False, "error": str(e)}, 400
    
    @app.route('/jwt/decode', methods=['POST'])
    def decode():
        try:
            if request.content_type is None or "application/json" not in request.content_type:
                return jsonify({"error": "Content-Type must be application/json"}), 400
            if not request.is_json:
                return jsonify({"error": "Invalid JSON"}), 400
            token = request.headers.get('Authorization')
            if token and token.startswith('Bearer '):
                token = token.split(' ')[1]
            if not token:
                return jsonify({"error": "Token is required"}), 400
            decoded = decode_token(token)
            if not decoded:
                return jsonify({"error": "Invalid token"}), 400
            return jsonify({"token": token, "decoded": decoded}), 200
        except Exception as e:
            return {"decoded": None, "error": str(e)}, 400
        
    @app.route('/jwt/refresh', methods=['POST'])
    def refresh():
        refresh_token = request.headers.get('Authorization')
        if refresh_token and refresh_token.startswith('Bearer '):
            refresh_token = refresh_token.split(' ')[1]
        try:
            decoded_refresh_token = decode_token(refresh_token)
            current_user = decoded_refresh_token['identity']
            new_token = create_access_token(identity=current_user)
            return jsonify({"access_token": new_token}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    
    @app.before_request
    def handle_options():
        if request.method == "OPTIONS":
            return '', 200


    @app.route('/')
    def home():
        return {"message": "Flask Backend API çalışıyor!"}, 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
