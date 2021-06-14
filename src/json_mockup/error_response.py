from json_mockup.base_class import BaseClass

class ErrorResponse(BaseClass):
    def __init__(self):
        self.error_msg = None

    def set_error_msg(self, msg):
        self.error_msg = msg