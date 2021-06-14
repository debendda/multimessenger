class FacebookMessengerNotLoggedInException(Exception):
    def __init__(self):
        self.msg = "The client is not logged in to facebook messenger."