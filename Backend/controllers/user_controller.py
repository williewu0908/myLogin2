from flask import Blueprint, request, jsonify, session
from models.users import User
from extensions import db
import uuid

# 建立一個 Blueprint
# 'auth' 是這個藍圖的名稱
# __name__ 是必需的
# url_prefix='/auth' 表示這個藍圖中的所有路由都會自動加上 /auth 前綴
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# 註冊
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    id = str(uuid.uuid4())
    username = data.get('userName') 
    user_true_name = data.get('userTrueName')
    password = data.get('password')
    email = data.get('email')
    
    if not username or not password:
        return jsonify({"msg": "缺少用戶名或密碼"}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "用戶名已存在"}), 400
    
    new_user = User(id=id, username=username, user_true_name=user_true_name, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "用戶註冊成功"}), 201

# 登入，如果登入成功，將使用者資訊存入 session
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        session['user_id'] = user.id
        session['username'] = user.username
        
        return jsonify({"msg": "登入成功", "user": {"username": user.username}})
    else:
        return jsonify({"msg": "帳號或密碼錯誤"}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"msg": "登出成功"}), 200

@auth_bp.route('/check_session', methods=['GET'])
def check_session():
    if 'user_id' in session:
        return jsonify(
            is_logged_in=True, 
            user={"username": session.get('username')}
        ), 200
    else:
        return jsonify(is_logged_in=False), 401

@auth_bp.route('/profile', methods=['GET'])
def protected_profile():
    if 'user_id' in session:
        return jsonify(
            logged_in_as=session.get('username'), 
            message="這裏是受保護的資料！"
        ), 200
    else:
        return jsonify({"msg": "未授權"}), 401