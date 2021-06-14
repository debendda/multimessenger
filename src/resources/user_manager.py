from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    current_user,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from models import UserModel
import helper 
import resources.user_manager_helper as UserManagerHelper

parser = reqparse.RequestParser()
parser.add_argument('mail', help='Mail address cannot be blank.', required=True)
parser.add_argument('password', help='Password cannot be blank.', required=True)

class Login(Resource):

    def post(self):
        data=parser.parse_args()
        current_user = UserModel.getUserByMail(data['mail'])

        if not current_user:
            return helper.get_message("Wrong credentials", 400)
        
        hash_password = UserModel.hashPassword(data['password'])
        if UserModel.hashEquals(hash_password, current_user.password):

            #block old access and refresh token
            if current_user.access_token:
                UserManagerHelper.revokeToken(current_user.access_token.jti)
            if current_user.refresh_token:
                UserManagerHelper.revokeToken(current_user.refresh_token.jti)

            #generate new access and refresh token and save them in db
            access_token = UserManagerHelper.generateAccessToken(current_user)
            refresh_token = UserManagerHelper.generateRefreshToken(current_user)
            
            current_user.update()

            return { 
                    'msg':'Successfully logged in',
                    'access_token':access_token,
                    'refresh_token':refresh_token
            }
        return helper.get_message("Wrong credentials", 400)

class UserLogoutAccess(Resource):

    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        try:
            #block access token
            UserManagerHelper.revokeToken(jti)

            return {'msg': 'Access token has been revoked'}

        except:
            return {'msg': 'Something went wrong'}, 500

class UserLogoutRefresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        jti = get_jwt()['jti']
        try:
            #block refresh token
            UserManagerHelper.revokeToken(jti)

            return {'msg': 'Refresh token has been revoked'}
        except:
            return {'msg': 'Something went wrong'}, 500

class TokenRefresh(Resource):

    @jwt_required(refresh=True)
    def post(self):
        user_mail = get_jwt_identity()
        current_user = UserModel.getUserByMail(user_mail)
        
        #block old access token and generate new one
        UserManagerHelper.revokeToken(current_user.access_token.jti)
        access_token = UserManagerHelper.generateAccessToken(current_user)

        current_user.update()

        return {'access_token': access_token}

