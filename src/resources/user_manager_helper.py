from flask_jwt_extended import decode_token, create_access_token, create_refresh_token

from models import RevokedTokenModel, AccessTokenModel, RefreshTokenModel

def generateAccessToken(user):
    access_token = create_access_token(identity=user.email)
    decoded_access_token = decode_token(access_token)
    access_token_model = AccessTokenModel(jti=decoded_access_token['jti'], exp=decoded_access_token['exp'])
    user.access_token = access_token_model

    return access_token

def generateRefreshToken(user):
    refresh_token = create_refresh_token(identity=user.email)
    decoded_refresh_token = decode_token(refresh_token)
    refresh_token_model = RefreshTokenModel(jti=decoded_refresh_token['jti'], exp=decoded_refresh_token['exp'])
    user.refresh_token = refresh_token_model
    
    return refresh_token

def revokeToken(jti):
    revoked_access_token = RevokedTokenModel(jti=jti)
    revoked_access_token.add()