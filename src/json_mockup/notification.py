from json_mockup.base_class import BaseClass

class MessageNotification(BaseClass):

    def __init__(self, author, message, messenger):
        self.author = author
        self.message = message
        self.event = "message"
        self.messenger = messenger

class MessageReadNotification(BaseClass):
    
    def __init__(self, timestamp, userid, messenger, chatid=None, messageid=None):
        self.timestamp = timestamp
        self.userid = userid
        self.chatid = chatid
        self.messageid = messageid
        self.event = "read"
        self.messenger = messenger

class MessageDeliveredNotification(BaseClass):

    def __init__(self, timestamp, message_id, userid, messenger):
        self.timestamp = timestamp
        self.message_id = message_id
        self.userid = userid
        self.event = "delivered"
        self.messenger = messenger

class UserTypingNotification(BaseClass):
    
    def __init__(self, userid, is_typing, messenger):
        self.is_typing = is_typing
        self.userid = userid
        self.event = "typing"
        self.messenger = messenger

class UserActiveNotification(BaseClass):

    def __init__(self, userid, last_active, active, messenger):
        self.userid = userid
        self.last_active = last_active
        self.active = active
        self.event = "active"
        self.messenger = messenger
 