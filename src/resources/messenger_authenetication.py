from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from app import fb_messenger, tg_messenger

login_parser = reqparse.RequestParser()
login_parser.add_argument('messenger', help='Messenger value cannot be blank.', required=True)
login_parser.add_argument('phone_number', help='Phonenumber is required for Telegram login', required=False)
login_parser.add_argument('email', help='Email cannot be blank.', required=False)
login_parser.add_argument('password', help='Password cannot be blank.', required=False)
login_parser.add_argument('code', help='Provide activation code if required', required=False)
login_parser.add_argument('api_id', help='Provide api_id for telegram', required=False)
login_parser.add_argument('api_hash', help='Provide api_hash for telegram', required=False)

class MessengerLogin(Resource):

    @jwt_required()
    def post(self):
        data = login_parser.parse_args(strict=True, http_error_code=400)
        messenger = data["messenger"]

        if(messenger == "facebook_messenger"):
            response = fb_messenger.login(data["email"], data["password"])
            return response.to_dict()
            
        if messenger == "telegram_messenger":
            response = tg_messenger.login(data['phone_number'], data['code'], data['password'], data['api_id'], data['api_hash'])
            return response.to_dict()
        else:
            return { 'msg' : f"Messenger '{messenger}' is not supported." }, 400

logout_parser = reqparse.RequestParser()
logout_parser.add_argument('messenger', help='Messenger value cannot be blank.', required=True)

class MessengerLogout(Resource):

    @jwt_required()
    def post(self):
        data = logout_parser.parse_args(strict=True, http_error_code=400)
        messenger = data["messenger"]
        
        if(messenger == "facebook_messenger"):
            response = fb_messenger.logout()
            return response.to_dict()
        if messenger == "telegram_messenger":
            response = tg_messenger.logout()
            return response.to_dict()

        return { 'message' : f"Messenger '{messenger}' is not supported." }, 400
