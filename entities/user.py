from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class AuthUser(db.Model):
    __tablename__ = 'auth_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    profile = db.relationship('User', back_populates='auth_user', uselist=False, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class User(db.Model):
    __tablename__ = 'user_profile'
    id = db.Column(db.Integer, primary_key=True)
    auth_user_id = db.Column(db.Integer, db.ForeignKey('auth_user.id', ondelete="CASCADE"), unique=True, nullable=False)
    auth_user = db.relationship('AuthUser', back_populates='profile')
    bloodType = db.Column(db.String(3), nullable=True)
    motorcycle = db.Column(db.String(50), nullable=True)
    partner = db.Column(db.String(50), nullable=True)
    godfather = db.Column(db.String(50), nullable=True)
    emergencyContact = db.Column(db.String(50), nullable=True)
    emergencyPhone = db.Column(db.String(50), nullable=True)
    formerMC = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    workAddress = db.Column(db.String(100), nullable=True)
    actualFunction = db.Column(db.String(50), nullable=False, default='Próspero')
    image_path = db.Column(db.String(256), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'auth_user_id': self.auth_user_id,
            'username': self.auth_user.username,
            'image_path': self.image_path,
            'bloodType': self.bloodType,
            'motorcycle': self.motorcycle,
            'partner': self.partner,
            'godfather': self.godfather,
            'emergencyContact': self.emergencyContact,
            'emergencyPhone': self.emergencyPhone,
            'formerMC': self.formerMC,
            'address': self.address,
            'workAddress': self.workAddress,
            'actualFunction': self.actualFunction
        }
