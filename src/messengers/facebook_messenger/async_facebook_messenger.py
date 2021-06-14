import fbchat
import datetime
from messengers.facebook_messenger.facebook_messenger_exception import FacebookMessengerNotLoggedInException
from messengers.facebook_messenger.facebook_messenger_notification_listener import FacebookNotificationListener
import threading

class AsyncFacebookMessenger:

    def __init__(self):
        self.session = None
        self.client = None
        self.notification_listener = FacebookNotificationListener()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args, **kwargs):
        return self

    def _check_logged_in(self):
        if not self.session:
            raise FacebookMessengerNotLoggedInException()

    async def login(self, email, password):
        self.session = await fbchat.Session.login(email, password)
        self.client = fbchat.Client(session=self.session)

        self._run_notification_listener(email, password)

    async def getAllUsers(self):
        self._check_logged_in()

        users = await self.client.fetch_users()
        return users

    async def getProfile(self, userid):
        self._check_logged_in()

        thread_infos = await self.client._fetch_info([userid])
        return thread_infos[userid]

    async def sendMessage(self, userid, message):
        self._check_logged_in()

        user = fbchat.User(session=self.session, id=userid)
        await user.send_text(message)

    async def getMessagesFromUser(self, userid):
        self._check_logged_in()

        user = fbchat.User(session=self.session, id=userid)
        messages = await user._fetch_messages(None, datetime.datetime.now())
        return messages

    async def logout(self): 
        self._check_logged_in()

        self._stop_notification_listener()
        
        await self.session.logout()
        self.session = None
        self.client = None


    def _run_notification_listener(self, email, password):
        thread = threading.Thread(target=self.notification_listener.run_listener, args=[email, password])
        thread.start()
    
    def _stop_notification_listener(self):
        self._check_logged_in()

        self.notification_listener.stop_listener()

  

