import asyncio
import fbchat
import queue
from messengers.facebook_messenger.facebook_messenger_notifications import FacebookMessengerNotifications

class FacebookNotificationListener():
    def __init__(self) -> None:
        self.client = fbchat.Client
        self.session = fbchat.Session
        self.listener = fbchat.Listener
        self.loop = asyncio.AbstractEventLoop
        self.q = queue.Queue(10)
        self.timeout = 1.0/60
        self.notifications = FacebookMessengerNotifications()
        
    def _on_thread(self, function, *args, **kwargs):
        self.q.put((function, args, kwargs))

    def run(self):
        while True:
            try:
                function, args, kwargs = self.q.get(timeout=self.timeout)
                function(*args, **kwargs)
            except queue.Empty:
                self.loop.run_until_complete(self.idle())

    async def idle(self):
        await asyncio.sleep(0.5)

    def run_listener(self, email, password):
        self.loop = asyncio.new_event_loop()
        self.loop.run_until_complete(self._init_listener(email, password))
    
    async def _init_listener(self, email, password):
        try:
            self.session = await fbchat.Session.login(email, password)
            self.listener = fbchat.Listener(session=self.session, chat_on=False, foreground=False)
            self.client = fbchat.Client(session=self.session)
            listen_task = asyncio.create_task(self._listen(self.listener))
            self.client.sequence_id_callback = self.listener.set_sequence_id
            await self.client.fetch_threads(limit=1).__anext__()
            await listen_task
            await self.session.logout()
        except Exception as ex:
            print(ex)

    async def _listen(self, listener):
        print("listen")
        async for event in listener.listen():
            #close listener if disconnect
            if isinstance(event, fbchat.Disconnect):
                print("Close Listener")
                return
            self.notifications.append_notification(event, self.session.user.id)
            

    def stop_listener(self):
        self._on_thread(self._stop_listen)

    def _stop_listen(self):
        self.listener.disconnect()