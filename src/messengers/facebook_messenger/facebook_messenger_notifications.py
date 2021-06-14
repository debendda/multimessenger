from json_mockup.notification import MessageDeliveredNotification, MessageNotification, MessageReadNotification, UserTypingNotification, UserActiveNotification
from json_mockup.messages import Message
from fbchat import ThreadsRead, MessagesDelivered, MessageEvent, Typing, Presence

class FacebookMessengerNotifications:
    
    @classmethod
    def append_notification(self, event, myid):
        from app import notification_handler
        messenger = "facebook_messenger"
        if isinstance(event, MessageEvent) and event.author.id != myid:
            message = Message(event.message.text, messenger, event.at.timestamp(), event.author.id)
            notification = MessageNotification(event.author.id, message, messenger)
            notification_handler.add_notification(notification)
            return
        
        elif isinstance(event, ThreadsRead):
            notification = MessageReadNotification(event.at.timestamp(), event.author.id, messenger)
            notification_handler.add_notification(notification)
            return 

        elif isinstance(event, MessagesDelivered):
            for message in event.messages:
                notification = MessageDeliveredNotification(event.at.timestamp(), message.id, event.author.id, messenger)
                notification_handler.add_notification(notification)
            return

        elif isinstance(event, Typing):
            notification = UserTypingNotification(event.author.id, event.status, messenger)
            notification_handler.add_notification(notification)
            return
        
        elif isinstance(event, Presence):
            for id in event.statuses:
                notification = UserActiveNotification(id, event.statuses[id].last_active.timestamp(), event.statuses[id].active, messenger)
                notification_handler.add_notification(notification)
            return

