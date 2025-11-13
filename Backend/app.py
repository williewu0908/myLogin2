import os
import redis
from flask import Flask
from extensions import db, bcrypt, cors, sess, mail, oauth
from controllers.user_controller import auth_bp
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

# 設定資料庫 URI
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 設定前端 BASE_URL
app.config['FRONTEND_BASE_URL'] = os.environ.get('FRONTEND_BASE_URL')

# 設置 SESSION 必要的 SECRET_KEY
app.config['SECRET_KEY'] = os.urandom(24)

# 設定 Flask-Session
app.config['SESSION_TYPE'] = 'redis'  # 告訴 Flask-Session 使用 redis
app.config['SESSION_PERMANENT'] = True  # 關閉瀏覽器仍不失效
app.config['SESSION_USE_SIGNER'] = True  # 對 session_id cookie 簽章
app.config['PERMANENT_SESSION_LIFETIME'] = 86400 # session 有效期為一天 (單位: 秒)
app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')

# --- 設定 Flask-Mail ---
app.config['MAIL_DEBUG'] = True
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

# 載入 Google OAuth 設定 ---
app.config['GOOGLE_CLIENT_ID'] = os.environ.get('GOOGLE_CLIENT_ID')
app.config['GOOGLE_CLIENT_SECRET'] = os.environ.get('GOOGLE_CLIENT_SECRET')

# 初始化擴充套件
db.init_app(app)
bcrypt.init_app(app)
# 設置 CORS (允許 Vue 帶 Cookie)
origins_list = ["http://localhost:5173", "http://140.127.74.15"]
cors.init_app(app, resources={r"/api/.*": {"origins": origins_list}}, supports_credentials=True)
sess.init_app(app)
mail.init_app(app)
oauth.init_app(app)

# --- 向 Authlib 註冊 Google ---
oauth.register(
    name='google',
    client_id=app.config.get('GOOGLE_CLIENT_ID'),
    client_secret=app.config.get('GOOGLE_CLIENT_SECRET'),
    # Authlib 會自動從這個 'OpenID Connect' URL 獲取所有需要的端點
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile' # 請求獲取 Email 和個人資料
    }
)

# 註冊藍圖
app.register_blueprint(auth_bp)

# # 建立資料庫 (關鍵)
# @app.before_first_request
# def create_tables():
#     db.create_all()


if __name__ == '__main__':
    app.run(debug=True, port=5000)