from json_mockup.base_class import BaseClass
from json import dumps

class GetChatRespose(BaseClass):

    def __init__(self):
        self.chats = []
        
    def append_chat(self, chat):
        self.chats.append(chat)
    
class GetProfilesResponse(BaseClass):
    def __init__(self):
        self.profiles = []

    def append_profile(self, profile):
        self.profiles.append(profile)

class SendMessageResponse(BaseClass):
    def __init__(self):
        self.msg = None

    def set_message(self, msg):
        self.msg = msg

class LogoutResponse(BaseClass):
    def __init__(self, messenger, msg):
        self.messenger = messenger
        self.msg = msg

class LoginResponse(BaseClass):
    def __init__(self, messenger, msg):
        self.messenger = messenger
        self.msg = msg
