import threading
import time

class NotificationHandler():

    def __init__(self):
        self.notifications = []
        self._lock = threading.Lock()

    def has_notifications(self):
        with self._lock:
            has_notifications = len(self.notifications) > 0
        return has_notifications

    def add_notification(self, notification):
        with self._lock:
            self.notifications.append(notification)

    def get_last_notification(self):
        with self._lock:
            notification = self.notifications.pop()
        return notification

    def listen(self):
        while True:
            if(self.has_notifications()):
                return self.get_last_notification()
            time.sleep(0.4)
        
