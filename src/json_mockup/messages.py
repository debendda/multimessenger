from json_mockup.base_class import BaseClass

class Message(BaseClass):

    def __init__(self, text, messenger, timestamp, author, message_id=None):
        self.text = text
        self.messenger = messenger
        self.timestamp = timestamp
        self.author = author
        self.message_id = message_id
