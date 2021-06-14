from json_mockup.base_class import BaseClass

class Chat(BaseClass):

    def __init__(self):
        self.userid = None
        self.messages = None
        self.title = None
    
    def set_title(self, title):
        self.title = title

    def set_user_id(self, id):
        self.userid = id    

    def append_message(self, message):
        if not self.messages:
            self.messages = []
        self.messages.append(message)

    def append_message_list(self, messages):
        for message in messages:
            self.append_message(message)