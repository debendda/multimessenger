import asyncio
from messengers.facebook_messenger.async_facebook_messenger import AsyncFacebookMessenger
from messengers.facebook_messenger.facebook_messenger_exception import FacebookMessengerNotLoggedInException
from json_mockup.profile import Profile
from json_mockup.chat import Chat
from json_mockup.messages import Message
from json_mockup.response import GetChatRespose, GetProfilesResponse, LoginResponse, LogoutResponse, SendMessageResponse
from json_mockup.profile import Profile
from json_mockup.error_response import ErrorResponse


class FacebookMessenger:
    def __init__(self):
        self.fb = AsyncFacebookMessenger()
        self.loop = asyncio.get_event_loop()
        #self.notification_loop = asyncio.new_event_loop()


    def login(self, email, password):
        try:
            self.loop.run_until_complete(self.fb.login(email, password))

            return LoginResponse("facebook_messenger", "Success.")
        except Exception as ex:
            print(ex)
            error = ErrorResponse()
            error.set_error_msg("Error while logging in to facebook messenger.")
            return error
    
    def logout(self):
        try:
            self.loop.run_until_complete(self.fb.logout())
            return LogoutResponse("facebook_messenger", "Success")
        except FacebookMessengerNotLoggedInException as ex:
            error = ErrorResponse()
            error.set_error_msg(ex.msg)
            return error
        except:
            error = ErrorResponse()
            error.set_error_msg("Error while logging out of facebook messenger.")
            return error

    def _getAllUsers(self):
        return self.loop.run_until_complete(self.fb.getAllUsers())

    def _getMessagesFromUser(self, userid):
        fb_messages = self.loop.run_until_complete(self.fb.getMessagesFromUser(userid))
        return_messages = []
        for message in fb_messages:
            return_message = Message(message.text, "facebook_messenger", message.created_at.timestamp(), message.author, message.id)
            return_messages.append(return_message)
        return return_messages

    def getChats(self):
        try:
            fb_users = self._getAllUsers()
            response = GetChatRespose()
            for user in fb_users:
                chat = self.getChat(user.id)
                response.append_chat(chat)
            return response
        except FacebookMessengerNotLoggedInException as ex:
            error = ErrorResponse()
            error.set_error_msg(ex.msg)
            return error
        except Exception as ex:
            print(ex)
            error = ErrorResponse()
            error.set_error_msg("Error while loading chats.")
            return error

    def getChat(self, userid):
        try:
            messages = self._getMessagesFromUser(userid)
            chat = Chat()
            chat.userid = userid
            chat.append_message_list(messages)
            return chat
        except FacebookMessengerNotLoggedInException as ex:
            error = ErrorResponse()
            error.set_error_msg(ex.msg)
            return error
        except:
            error = ErrorResponse()
            error.set_error_msg("Error while loading chat.")
            return error

    def getProfile(self, userid):
        try:
            fb_profile = self.loop.run_until_complete(self.fb.getProfile(userid))
            profile = Profile("facebook_messenger")
            profile.set_name(fb_profile["name"])
            profile.set_user_id(fb_profile["id"])
            profile.set_profile_picture_uri(fb_profile['profile_picture']['uri'])
            profile.set_profile_url(fb_profile["url"])
            return profile
        except FacebookMessengerNotLoggedInException as ex:
            error = ErrorResponse()
            error.set_error_msg(ex.msg)
            return error
        except:
            error = ErrorResponse()
            error.set_error_msg("Error while loading profile.")
            return error

    def getProfiles(self):
        try:
            fb_users = self._getAllUsers()
            profiles = GetProfilesResponse()
            for fb_user in fb_users:
                profile = self.getProfile(fb_user.id)
                profiles.append_profile(profile)
            return profiles
        except FacebookMessengerNotLoggedInException as ex:
            error = ErrorResponse()
            error.set_error_msg(ex.msg)
            return error
        except:
            error = ErrorResponse()
            error.set_error_msg("Error while loading profiles.")
            return error

    def saveSession(self):
        self.fb.saveSession()

    def sendMessage(self, userid, message):
        try:
            self.loop.run_until_complete(self.fb.sendMessage(userid, message))#self.__async__send_message(user, message))
            response = SendMessageResponse()
            response.set_message("Successfully send message.")
            return response
        except FacebookMessengerNotLoggedInException as ex:
            error = ErrorResponse()
            error.set_error_msg(ex.msg)
            return error
        except:
            error = ErrorResponse()
            error.set_error_msg("Error while sending message.")
            return error
