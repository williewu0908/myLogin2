from itsdangerous import URLSafeTimedSerializer
from flask import current_app

# 建立一個令牌產生器
def get_reset_token_serializer():
    """
    建立一個用於密碼重設的、有時效的序列化器。
    """
    return URLSafeTimedSerializer(
        current_app.config['SECRET_KEY'],
        salt='password-reset-salt' # (重要) 使用鹽 (salt) 確保此令牌只能用於密碼重設
    )