from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from app import fb_messenger, tg_messenger

get_profile_parser = reqparse.RequestParser()
get_profile_parser.add_argument('messenger', help='Messenger value cannot be blank.', required=True)
get_profile_parser.add_argument('userid', required=False)

class Profiles(Resource):

    @jwt_required()
    def get(self):
        data = get_profile_parser.parse_args(strict=True, http_error_code=400)
        messenger = data["messenger"]
        userid = data["userid"]

        if messenger == "facebook_messenger":
            if not userid:
                # send all profiles
                profiles = fb_messenger.getProfiles()
                return profiles.to_dict()
            # send specific profile with userid
            profile = fb_messenger.getProfile(userid)
            return profile.to_dict()
            
        if messenger == "telegram_messenger":
            if not userid:
                profiles = tg_messenger.get_profiles()
                return profiles.to_dict()
            profile = tg_messenger.get_profile(userid)
            return profile.to_dict()

        return { "message" : f"Messenger '{messenger}' is not supported."}
        
        
