class TelegramMessengerNoSessionException(Exception):
    def __init__(self):
        self.msg = "The client is not logged in to telegram messenger"