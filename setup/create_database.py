from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
import hashlib
from getpass import getpass
from os import path

database_name = "users.sqlite3"
database_path = f"../src/{database_name}"

print()
print("-------------------------------")
print("Creating Database")
print("-------------------------------")
print()

base = declarative_base()
engine = sa.create_engine(f"sqlite:///{database_path}")
base.metadata.bind = engine
session = orm.scoped_session(orm.sessionmaker())(bind=engine)

class UserModel(base):

    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key = True)
    password = sa.Column(sa.String(255), nullable = False)
    email = sa.Column(sa.String(255), unique=True, nullable=False)
    access_token = orm.relationship("AccessTokenModel", uselist=False, back_populates='user')
    refresh_token = orm.relationship("RefreshTokenModel", uselist=False, back_populates='user')

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
        session.commit()

    def save(self):
        session.add(self)
        session.commit()

class RevokedTokenModel(base):
     
    __tablename__ = 'revoked_tokens'

    id = sa.Column('revoked_tokens', sa.Integer, primary_key = True)
    
    jti = sa.Column(sa.String(120))

    def add(self):
        sa.session.add(self)
        sa.session.commit()

    @classmethod
    def is_jti_blocklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)

class AccessTokenModel(base):

    __tablename__ = 'access_token'

    id = sa.Column(sa.Integer, primary_key=True)
    jti = sa.Column(sa.String(120))
    exp = sa.Column(sa.Integer)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    user = orm.relationship("UserModel", back_populates="access_token")


class RefreshTokenModel(base):

    __tablename__ = 'refresh_token'

    id = sa.Column(sa.Integer, primary_key=True)
    jti = sa.Column(sa.String(120))
    exp = sa.Column(sa.Integer)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    user = orm.relationship("UserModel", back_populates="refresh_token")


if path.exists(database_path):
    print("-------------------------------")
    print("Database allready exists.")
    print("-------------------------------")
    print()
    exit(0)

base.metadata.create_all()
print("Created database and tables")
print()
print()
print("User Setup.")
user_email = input("Please enter your email address: ")

while True:
    password = getpass("Please enter your password: ")
    password1 = getpass("Please repeate your password: ")
    if password == password1:
        break
    print("The passwords do not match. Please try again.")

user = UserModel(user_email, UserModel.hashPassword(password))
user.save()

print()
print("-------------------------------")
print("Registration was successfull.")
print("-------------------------------")
print()
