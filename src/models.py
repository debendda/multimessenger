from app import db
from sqlalchemy.orm import relationship
import hashlib

def create_db():
    db.create_all()

class UserModel(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    password = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    access_token = relationship("AccessTokenModel", uselist=False, back_populates='user')
    refresh_token = relationship("RefreshTokenModel", uselist=False, back_populates='user')

    def __init__ (self, email, password):
        self.email = email
        self.password = password

    @classmethod
    def getUserByMail(cls, email):
        return cls.query.filter_by(email=email).first()

    @staticmethod
    def hashPassword(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def hashEquals(new_hash, hash):
        return new_hash == hash

    def update(self):
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

class RevokedTokenModel(db.Model):
     
    __tablename__ = 'revoked_tokens'

    id = db.Column('revoked_tokens', db.Integer, primary_key = True)
    
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blocklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)

class AccessTokenModel(db.Model):

    __tablename__ = 'access_token'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))
    exp = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("UserModel", back_populates="access_token")


class RefreshTokenModel(db.Model):

    __tablename__ = 'refresh_token'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))
    exp = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("UserModel", back_populates="refresh_token")
