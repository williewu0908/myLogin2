from flask import Flask, request, jsonify, session # 導入 session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS # 導入 CORS
import os

# --- 應用程式配置 ---
app = Flask(__name__)

# 配置 CORS:
# 1. 允許來自 Vue 開發伺服器的請求
# 2. 必須設置 supports_credentials=True 才能允許跨域 Cookie
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}}, supports_credentials=True)

# 配置資料庫
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# 配置 Session 所需的 SECRET_KEY，用於簽名 session cookie
# 這在 Session 模式下是 *必須* 的
app.config['SECRET_KEY'] = os.urandom(24) # 'your-very-strong-secret-key'

# (可選) Flask 預設將 session 儲存在 *客戶端* 的 cookie 中 (有簽名，但非加密)
# 如果您希望將 session 儲存在伺服器端 (更安全，可儲存更多資料):
# app.config['SESSION_TYPE'] = 'filesystem' # 或 'sqlalchemy', 'redis'
# from flask_session import Session
# Session(app)


# --- 初始化擴充套件 ---
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# --- 資料庫模型 (Model) ---
# (與 JWT 版本的 User Model 相同)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

@app.before_first_request
def create_tables():
    db.create_all()

# --- API 路由 (Routes) ---

# 1. 註冊路由 (相同)
@app.route('/api/register', methods=['POST'])
def register():
    # ... (註冊邏輯與 JWT 版本相同) ...
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"msg": "缺少用戶名或密碼"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "用戶名已存在"}), 400
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "用戶註冊成功"}), 201


# 2. 登入路由 (已修改)
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        # 登入成功：將用戶資訊存入伺服器 session
        # Flask 會自動發送 Set-Cookie 標頭
        session['user_id'] = user.id
        session['username'] = user.username
        
        return jsonify({"msg": "登入成功", "user": user.username})
    else:
        return jsonify({"msg": "帳號或密碼錯誤"}), 401

# 3. 登出路由 (Session 模式下*必須*)
@app.route('/api/logout', methods=['POST'])
def logout():
    # 清除伺服器端的 session
    session.pop('user_id', None)
    session.pop('username', None)
    # session.clear() # 或清除所有
    return jsonify({"msg": "登出成功"}), 200

# 4. 受保護的路由 (已修改)
# (不再需要 @jwt_required)
@app.route('/api/profile', methods=['GET'])
def protected_profile():
    # 檢查 'user_id' 是否存在於伺服器 session 中
    if 'user_id' in session:
        return jsonify(
            logged_in_as=session['username'], 
            message="這裏是受保護的資料！"
        ), 200
    else:
        # 如果 session 中沒有，代表未登入
        return jsonify({"msg": "未授權"}), 401

# 5. (推薦) 用於 Vue 啟動時檢查登入狀態的路由
@app.route('/api/check_session', methods=['GET'])
def check_session():
    if 'user_id' in session:
        return jsonify(
            is_logged_in=True, 
            user=session['username']
        ), 200
    else:
        return jsonify(is_logged_in=False), 401


if __name__ == '__main__':
    app.run(debug=True, port=5000)