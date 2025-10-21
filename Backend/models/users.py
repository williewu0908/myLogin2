# models/users.py
from extensions import db, bcrypt

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(64), primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    user_true_name = db.Column(db.String(32), nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False) 

    def __init__(self, id, username, user_true_name, password, email):
        self.id = id
        self.username = username
        self.user_true_name = user_true_name
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        self.email = email

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)