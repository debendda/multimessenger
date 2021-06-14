from json_mockup.base_class import BaseClass

class Profile(BaseClass):

    def __init__(self, messenger):
        self.userid = None
        self.name = None
        self.number = None
        self.email = None
        self.profile_picture_uri = None
        self.messenger = messenger
        self.profile_url = None

    def set_user_id(self, id):
        self.userid = id    

    def set_name(self, name):
        self.name = name
    
    def set_number(self, number):
        self.number = number
    
    def set_email(self, email):
        self.email = email
    
    def set_profile_picture_uri(self, uri):
        self.profile_picture_uri = uri
    
    def set_messenger(self, messenger):
        self.messenger = messenger
    
    def set_profile_url(self, url):
        self.profile_url = url
