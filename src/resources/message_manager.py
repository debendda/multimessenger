from flask import Response
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from app import fb_messenger, tg_messenger, notification_handler

class MessageEvent(Resource):

    @jwt_required()
    def get(self):
        def eventStream():
            notification = notification_handler.listen()
            yield 'data: {}\n\n'.format(notification.to_dict())
        return Response(eventStream(), mimetype="text/event-stream")

get_message_parser = reqparse.RequestParser()
get_message_parser.add_argument('messenger', help='Messenger value cannot be blank.', required=True)
get_message_parser.add_argument('userid', required=False)

send_msg_parser = reqparse.RequestParser()
send_msg_parser.add_argument('messenger', help='Messenger cannot be blank.', required=True)
send_msg_parser.add_argument('userid', help='User ID cannot be blank.', required=True)
send_msg_parser.add_argument('message', help='Message cannot be blank.', required=True)

class Chats(Resource):

    @jwt_required()
    def get(self):
        data = get_message_parser.parse_args(strict=True, http_error_code=400)
        messenger = data["messenger"]
        userid = data["userid"]

        if messenger == "facebook_messenger":
            # send all chats
            if not userid:
                chats = fb_messenger.getChats()
                return chats.to_dict()
            #send chat from user with userid 
            single_chat = fb_messenger.getChat(userid)
            return single_chat.to_dict()
        if messenger == "telegram_messenger":
            if not userid:
                chats = tg_messenger.get_all_chats()
                return chats.to_dict()
            single_chat = tg_messenger.get_chat(userid)
            return single_chat.to_dict()

        return { "message" : f"Messenger '{messenger}' is not supported."}

    @jwt_required()
    def post(self):
        data = send_msg_parser.parse_args(strict=True, http_error_code=400)
        messenger = data["messenger"]
        if messenger == "facebook_messenger":
            response = fb_messenger.sendMessage(data["userid"], data["message"])
            return response.to_dict()
        if messenger == "telegram_messenger":
            response = tg_messenger.send_message(data['userid'], data['message'])
            return response.to_dict()
        return { "message" : f"Messenger '{messenger}' is not supported."}
