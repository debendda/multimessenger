from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from datetime import timedelta
from messengers.telegram_messenger.telegram_messenger import TelegramMessenger
from notification_handler import NotificationHandler
import ssl
import models
from messengers.facebook_messenger.facebook_messenger import FacebookMessenger
from notification_handler import NotificationHandler
import nest_asyncio
nest_asyncio.apply()

app = Flask(__name__)
CORS(app)

api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SECRET_KEY'] = "salty"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JWT_SECRET_KEY'] = 'salty2'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=4)
app.config['PROPAGATE_EXCEPTIONS'] = True

context = ssl.SSLContext(ssl.PROTOCOL_TLS)
context.load_cert_chain('../key/cert.pem', '../key/key.pem')

db = SQLAlchemy(app)

jwt = JWTManager(app)

fb_messenger = FacebookMessenger()
tg_messenger = TelegramMessenger()

notification_handler = NotificationHandler()

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):

    jti = jwt_payload['jti']
    return models.RevokedTokenModel.is_jti_blocklisted(jti)


if __name__ == "__main__":
    from models import create_db
    from resources.user_manager import Login, UserLogoutAccess, UserLogoutRefresh, TokenRefresh
    from resources.message_manager import MessageEvent, Chats
    from resources.messenger_authenetication import MessengerLogin, MessengerLogout
    from resources.profile_manager import Profiles
    
    create_db()

    api.add_resource(Login, '/login')
    api.add_resource(MessageEvent, '/stream')
    api.add_resource(UserLogoutAccess, '/logout/access')
    api.add_resource(UserLogoutRefresh, '/logout/refresh')
    api.add_resource(TokenRefresh, '/token/refresh')
    api.add_resource(MessengerLogin, '/messenger/login')
    api.add_resource(MessengerLogout, '/messenger/logout')
    api.add_resource(Chats, '/messenger/chats')
    api.add_resource(Profiles, '/messenger/profiles')

    app.run(ssl_context=context,threaded=True)