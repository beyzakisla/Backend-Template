from flask import jsonify
from services.auth_service import register_user, login_user, generate_reset_token, verify_reset_token, update_password, delete_api_key, generate_api_key
from models.user_model import User, ApiKey, db

class UserController:
    @staticmethod
    def register(username, password, email, name, surname):
        """
        Kullanıcı kaydını yönetir.
        """
        if not username or not password:
            raise ValueError("Username ve password alanları zorunludur.")

        if len(username) < 3 or len(username) > 20:
            raise ValueError("Kullanıcı adı 3 ile 20 karakter arasında olmalıdır.")
        
        if not email:
            raise ValueError("Email alanı zorunludur.")
        
        if len(password) < 6:
            raise ValueError("Şifre en az 6 karakter uzunluğunda olmalıdır.")

        return register_user(username, password, email, name, surname)

    @staticmethod
    def login(username, password):
        """
        Kullanıcı girişini yönetir.
        """
        if not username or not password:
            raise ValueError("Username ve password alanları zorunludur.")

        return login_user(username, password)
    
    @staticmethod
    def request_password_reset(email):
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        token = generate_reset_token(user.id)
        # Burada email gönderimi yapılabilir
        print(f"Password reset token for {email}: {token}")  # Debug için
        return jsonify({"message": "Password reset email sent", "token": token}), 200

    @staticmethod
    def reset_password(token, new_password):
        user_id = verify_reset_token(token)
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 400

        if update_password(user_id, new_password):
            return jsonify({"message": "Password has been reset successfully"}), 200
        return jsonify({"error": "Password reset failed"}), 500
    
    @staticmethod
    def generate_api_key(user_id, expiration_time_in_days):
        return generate_api_key(user_id, expiration_time_in_days)

    @staticmethod
    def delete_api_key(api_key_id):
        try:
            api_key = ApiKey.query.filter_by(id=api_key_id).first()

            if not api_key:
                return False
            
            db.session.delete(api_key)
            db.session.commit()
            return True
        except Exception as e:
            print(f"Error deleting API key: {str(e)}")
            return False
