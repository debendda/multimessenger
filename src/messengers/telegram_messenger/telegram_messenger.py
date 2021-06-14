from telegram.client import Telegram
from telegram.client import AuthorizationState
from messengers.telegram_messenger.telegram_messenger_exception import TelegramMessengerNoSessionException

from json_mockup.notification import MessageNotification, MessageReadNotification
from json_mockup.profile import Profile
from json_mockup.chat import Chat
from json_mockup.messages import Message
from json_mockup.response import GetChatRespose, GetProfilesResponse, LoginResponse, LogoutResponse, SendMessageResponse
from json_mockup.error_response import ErrorResponse

class TelegramMessenger:
    def __init__(self):
        self.tg_session = None
        self.logged_in = False

    def _check_session(self):
        if not self.logged_in:
            raise TelegramMessengerNoSessionException()

    def update_chat_read_output(self, update):
        from app import notification_handler
        chat_id = update['chat_id']
        last_read_outbox_message_id = update['last_read_outbox_message_id']
        notification = MessageReadNotification(None, None, "telegram_messenger", chatid=str(chat_id), messageid=str(last_read_outbox_message_id)) 
        notification_handler.add_notification(notification)
        return

    def update_message_handler(self, update):
        from app import notification_handler
        message = update['message']
        if message['is_outgoing']:
            return
        message_id = str(message['id'])
        author = str(message['sender'].get('user_id', ''))
        chat_id = str(message['chat_id'])
        timestamp = message['date']
        message_content = message['content']
        text = message_content.get('@type')
        # Set type as text, if type is text then overwrite and add the actual text
        if text == "messageText":
            text = message_content.get('text').get('text', '')
        tg_message = Message(text, "telegram_messenger", timestamp, author, message_id=message_id)
        notification = MessageNotification(author, tg_message, "telegram_messenger")
        notification_handler.add_notification(notification)
        return

    def login(self, phone_number, code=None, password=None, api_id=None, api_hash=None):
        try:
            if (api_id is None or api_hash is None) and self.tg_session is None:
                error = ErrorResponse()
                error.set_error_msg("Supply a api_id and api_hash in your request")
                return error
            
            if self.tg_session is not None and self.logged_in:
                error = ErrorResponse()
                error.set_error_msg("Client already has a active session")
                return error

            self.tg_session = Telegram(
                api_id = api_id,
                api_hash = api_hash,
                phone = phone_number,
                database_encryption_key='SuperSecretKey',
                tdlib_verbosity=0,
            )
            state = self.tg_session.login(blocking=False)
            if state == AuthorizationState.WAIT_CODE:
                if code is None:
                    self.tg_session.stop()
                    error = ErrorResponse()
                    error.set_error_msg("Error while login to telegram messenger. Code required")
                    return error
                self.tg_session.send_code(code)
                state = self.tg_session.login(blocking=False)
            if state == AuthorizationState.WAIT_PASSWORD:
                if password is None:
                    self.tg_session.stop()
                    error = ErrorResponse()
                    error.set_error_msg("Error while login to telegram messenger. Password required")
                    return error
                self.tg_session.send_password(password)
                state = self.tg_session.login(blocking=False)
            if state == AuthorizationState.READY:
                self.logged_in = True
                # Need to call this function in order to fetch all chats online because get_chat is an offline call
                result = self.tg_session.get_chats(9223372036854775807)
                result.wait()
                self.tg_session.add_update_handler("updateChatReadOutbox", self.update_chat_read_output)
                self.tg_session.add_message_handler(self.update_message_handler)
                return LoginResponse("telegram_messenger", "Success.")

        except ValueError as ex:
            if self.tg_session is not None:
                self.logged_in = False
                self.tg_session.stop()
            error = ErrorResponse()
            error.set_error_msg(str(ex))
            return error
        except Exception as ex:
            if self.tg_session is not None:
                self.logged_in = False
                self.tg_session.stop()
            error = ErrorResponse()
            error.set_error_msg("Error while login to Telegram messenger")
            return error

    def logout(self):
        try:
            self._check_session()
            self.tg_session.stop()
            self.logged_in = False
            return LogoutResponse("telegram_messenger", "Success")
        except TelegramMessengerNoSessionException as ex:
            error = ErrorResponse()
            error.set_error_msg(ex.msg)
            return error
        except:
            error = ErrorResponse()
            error.set_error_msg("Error with logout from telegram messenger")
            return error

    def get_chat(self, chat_id):
        try:
            self._check_session()
            res = self.tg_session.get_chat(chat_id)
            res.wait()

            chat = Chat()
            chat.set_user_id(str(res.update['id']))
            chat.set_title(res.update['title'])
            messages = self.get_messages_from_chat(chat_id)
            chat.append_message_list(messages)
            return chat
        except TelegramMessengerNoSessionException as ex:
            error = ErrorResponse()
            error.set_error_msg(ex.msg)
            return error
        except:
            error = ErrorResponse()
            error.set_error_msg("Error while loading chat")
            return error

    def get_messages_from_chat(self, chat_id):
        try:
            self._check_session()
            messages = self.tg_session.get_chat_history(chat_id)
            messages.wait()

            messages = messages.update['messages']
            return_messages = []
            for message in messages:
                sender_id = message['sender'].get('user_id', '')
                # Had some messages without id, don't know why, but if so, continue
                if not sender_id:
                    continue
                message_content = message['content'].get('text', {})
                # Content can be a call or data. If there is no text, continue.
                if message_content is None:
                    continue
                message_text = message_content.get('text', '')
                timestamp = message['date']
                return_message = Message(message_text, "Telegram", timestamp, str(sender_id), message_id=str(message['id']))
                return_messages.append(return_message)
            return return_messages
        except TelegramMessengerNoSessionException as ex:
            error = ErrorResponse()
            error.set_error_msg(ex.msg)
            return error
        except:
            error = ErrorResponse()
            error.set_error_msg("Error while loading chat")
            return error
    
    def get_all_chats(self):
        try:
            self._check_session()
            result = self.tg_session.get_chats(9223372036854775807)
            result.wait()

            chat_ids = result.update['chat_ids']
            response = GetChatRespose()
            for chat_id in chat_ids:
                chat = self.get_chat(chat_id)
                response.append_chat(chat)
            return response
        except TelegramMessengerNoSessionException as ex:
            error = ErrorResponse()
            error.set_error_msg(ex.msg)
            return error
        except:
            error = ErrorResponse()
            error.set_error_msg("Error while loading chat")
            return error
    
    def get_profile(self, user_id):
        try:
            self._check_session()
            result = self.tg_session.get_user(user_id)
            result.wait()
            profile = Profile("telegram_messenger")
            content = result.update
            if content['first_name'] and content['last_name']:
                name = content['first_name'] + " " + content['last_name']
            elif content['first_name']:
                name = content['first_name']
            elif content['last_name']:
                name = content['last_name']
            elif content['username']:
                name = content['username']
            number = content['phone_number']
            profile.set_name(name)
            profile.set_number(number)
            profile.set_user_id(user_id)
            return profile
        except TelegramMessengerNoSessionException as ex:
            error = ErrorResponse()
            error.set_error_msg(ex.msg)
            return error
        except:
            error = ErrorResponse()
            if int(user_id) < 0:
                error.set_error_msg("Groups can't be fetched")
            else:
                error.set_error_msg("Error while loading Profile")
            return error

    def get_profiles(self):
        try:
            self._check_session()
            chats = self.tg_session.get_chats(9223372036854775807)
            chats.wait()
            chat_ids = chats.update['chat_ids']
            # Negative chat_ids are groups and supergroups. There is no profile to fetch
            chat_ids = [_id for _id in chat_ids if _id > 0]
            profiles = GetProfilesResponse()
            for _id in chat_ids:
                profile = self.get_profile(_id)
                profiles.append_profile(profile)
            return profiles
        except TelegramMessengerNoSessionException as ex:
            error = ErrorResponse()
            error.set_error_msg(ex.msg)
            return error
        except:
            error = ErrorResponse()
            error.set_error_msg("Error while loading profiles")
            return error

    def send_message(self, user_id, message):
        try:
            self._check_session()
            self.tg_session.send_message(user_id, message)
            response = SendMessageResponse()
            response.set_message("Successfully send message.")
            return response
        except TelegramMessengerNoSessionException as ex:
            error = ErrorResponse()
            error.set_error_msg(ex.msg)
            return error
        except:
            error = ErrorResponse()
            error.set_error_msg("Error while sending message.")
            return error