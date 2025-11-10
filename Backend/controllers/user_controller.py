from flask import Blueprint, request, jsonify, session, current_app, redirect, url_for
from flask_mail import Message
from models.users import User
from extensions import db, mail, bcrypt, oauth
import uuid
from services.authService import get_reset_token_serializer

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
    

    
@auth_bp.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    username = data.get('userName')
    email = data.get('Email')
    
    # 基本驗證
    if not email or not username:
        return jsonify({"msg": "缺少必要資訊"}), 400

    # 查詢同時匹配 username 和 email 的使用者
    user = User.query.filter_by(username=username, email=email).first()

    # 只有當帳號和 Email 都匹配時，才會執行
    if user:
        # 產生令牌
        s = get_reset_token_serializer()
        token = s.dumps(user.email, salt='password-reset-salt') 

        # 建立前端重設 URL
        current_url = current_app.config.get('FRONTEND_BASE_URL')
        reset_url = f"{current_url}/resetPassword?token={token}"

        # 發送 Email
        try:
            msg = Message(
                subject="[EduTools] 密碼重設請求",
                recipients=[user.email],
                body=f"您好，請點擊以下連結來重設您的密碼：\n{reset_url}\n\n如果您沒有請求重設，請忽略此郵件。"
            )
            mail.send(msg)
        except Exception as e:
            current_app.logger.error(f"Email 發送失敗: {e}")
    else:
        return jsonify({"msg": "使用者帳號或Email不存在"})

    return jsonify({"msg": "重設連結已發送至該信箱。"}), 200



# 提交新密碼
@auth_bp.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('password')

    s = get_reset_token_serializer()
    
    try:
        # 驗證令牌 (時效預設 1 小時)
        # 這裡會檢查 1. 簽章 2. Salt 3. 時效
        email = s.loads(token, salt='password-reset-salt', max_age=3600) # 3600 秒 = 1 小時
        
    except Exception as e:
        return jsonify({"msg": "您的重設連結無效或已過期。"}), 400

    # 令牌有效，找到使用者並更新密碼
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"msg": "使用者不存在。"}), 404 # 理論上不該發生

    # 雜湊新密碼並儲存
    user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
    db.session.commit()

    return jsonify({"msg": "密碼已成功重設！"}), 200





# --- Google 登入 ---
@auth_bp.route('/google/login')
def google_login():
    # 產生回呼 URL
    # 'auth.google_callback' 指的是 'auth' 藍圖下的 'google_callback' 函式
    redirect_uri = url_for('auth.google_callback', _external=True)
    
    # 使用 Authlib 產生 Google 登入頁面的 URL 並重新導向使用者
    return oauth.google.authorize_redirect(redirect_uri)


# --- 處理 Google 的回呼 ---
@auth_bp.route('/google/callback')
def google_callback():
    try:
        # 取得 Access Token
        token = oauth.google.authorize_access_token()
        
        # 獲取使用者資訊
        # 'userinfo' 是 OpenID Connect (OIDC) 的標準欄位
        user_info = token.get('userinfo')

        if not user_info or not user_info.get('email'):
            return jsonify({"msg": "從 Google 獲取 Email 失敗"}), 400

        email = user_info.get('email')
        name = user_info.get('name')

        # 檢查使用者是否存在 
        user = User.query.filter_by(email=email).first()

        if not user:
            # 使用者不存在，自動為他註冊
            
            # 使用 Email 的 @ 符號前部分作為基本 username
            username = email.split('@')[0]
            if User.query.filter_by(username=username).first():
                username = username + str(uuid.uuid4())[:4]
                
            # 產生一個隨機、無法被登入的密碼
            random_password = str(uuid.uuid4())
            
            user = User(
                id=str(uuid.uuid4()),
                username=username,
                user_true_name=name,
                password=random_password,
                email=email
            )
            db.session.add(user)
            db.session.commit()

        # 登入使用者 (寫入 Session)
        session['user_id'] = user.id
        session['username'] = user.username

        # 重新導向回 Vue 首頁
        current_url = current_app.config.get('FRONTEND_BASE_URL')
        return redirect(f"{current_url}/home")

    except Exception as e:
        current_app.logger.error(f"Google OAuth 回呼失敗: {e}")
        return jsonify({"msg": "快速登入失敗"}), 400