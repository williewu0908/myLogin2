import os
import redis
from flask import Flask
from extensions import db, bcrypt, cors, sess
from controllers.user_controller import auth_bp

app = Flask(__name__)

# 設置資料庫 URI
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'mysql+pymysql://cph_server:cph20251021@localhost/mylogindb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 設置 SESSION 必要的 SECRET_KEY
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(24)

# 設定 Flask-Session
app.config['SESSION_TYPE'] = 'redis'  # 告訴 Flask-Session 使用 redis
app.config['SESSION_PERMANENT'] = False  # 關閉瀏覽器就失效
app.config['SESSION_USE_SIGNER'] = True  # 對 session_id cookie 簽章
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')

# 初始化擴充套件
db.init_app(app)
bcrypt.init_app(app)
# 設置 CORS (允許 Vue 帶 Cookie)
cors.init_app(app, resources={r"/auth/*": {"origins": "http://localhost:8080"}}, supports_credentials=True)
sess.init_app(app)

# 註冊藍圖
app.register_blueprint(auth_bp)

# # 建立資料庫 (關鍵)
# @app.before_first_request
# def create_tables():
#     db.create_all()


if __name__ == '__main__':
    app.run(debug=True, port=5000)