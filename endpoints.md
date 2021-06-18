# Endpoint description



## API 

### Common Errors
#### Missing Parameter
```
{
    "message": {
        "mail": "<Parameter Name> cannot be blank"
    }
}
```
#### Missing or Wrong Tokens
When using an access token, where only refersh tokens are allowed, following messages will be send
```
{
    "msg": "Only refresh tokens are allowed"
}
```
```
{
    "msg": "Only non-refresh tokens are allowed"
}
```

If the Signature field from the Token is missing 
```
{
    "msg": "Signature verification failed"
}
```

In case the token expired:
```
{
    "msg": "Token has expired"
}
```

If the complete Authorization Header is missing:
```
{
    "msg": "Missing Authorization Header"
}
```

### Login
In order to Login a Request to */login* should look like this 
```
{
    "email": <str>,
    "password": <str>
}
```

If the login was succesful you'll recieve the access and refresh token
```
{
    "msg": "Successfully logged in", 
    "access_token": <string>,
    "refresh_token": <string>
}
```

### Refresh Access token
If the access token is expired, send a Post Request to */token/refresh*:
```
{
    "refresh_token": <str>
}
```

In case the Request was successful the Response will be a new access_token
```
{
    "access_token": <str>
}
```
### Logout
In order to logout from the API the access and refresh token should be revoked. So nobody will be able to use them later.
To revoke the Access Token, a Post Request to */logout/access* should be sent. 
A Request to */logout/refresh* will revoke the refresh Token.

Both endpoints only take the corresponding token. 

## Messenger

### Login
The endpoint */login/messenger* is used to authenticate and login the corresponding Messenger. 
This endpoint takes seven Parameters for each Post Request:
- **messenger**: String, defines the messenger *telegram_messenger* or *facebook_messenger*
- **phone_number**: String, Optional, used for *telegram_messenger*
- **email**: String, Optional, only used to login to *facebook_messenger*
- **password**: String, Optional, necessary if 2FA for Telegram is activated
- **code**: String, Optional, is the authorization code sent from Telegram Service
- **api_id**: String, Optional, transmits the API_ID obtained from Telegram
- **api_hash**: String, Optional, is the API_HASH obtained from Telegram

If the Login was successful:
```
{
    "messenger": <str>,
    "msg": "Login successful"
}
```

### Telegram
To Login to Telegram send a Post Request
```
{
    "messenger": "telegram_messenger",
    "phone_number": <str>,
    "api_id": <str>,
    "api_hash": <str>
}
```
If this is the first Login following Error Message will be recieved
```
{
    "error_msg": "Error while login to telegram messenger. Code required"
}
```

If the code from Telegram Service was recieved, send a new Request with the code in the code parameter field. 

In case the login was succesful:
```
{
    "messenger": "telegram_messenger",
    "msg": "Success"
}
```

### Facebook
When login to Facebook send following Request to */login/messenger*.
```
{
    "messenger": "facebook_messenger",
    "email": <str>,
    "password": <str>
}
```

If the Login credentials are correct:
```
{
    "messenger": "facebook_messenger",
    "msg": "Success"
}
```

### Login
To logout from a messenger send a Post Request to */messenger/logout*.
```
{
    "messenger": <str>
}
```
When everything was correct:
```
{
    "messenger": <str>,
    "msg": "Success"
}
```

### Chats
With the endpoint */messenger/chats* with Post Requests Messages can be send. Get Request will pull all or single chats from the corresponding messenger.
This endpoint takes following parameters:
- **messenger**: String, needed. Defines which messenger should be used to send or recieve messages
- **userid**: String, optional. If a user_id is given, only the chats from that user will be pulled or a message will be sent to this user. If none is given all messages will be recieved
- **message**: String, optional. Used if a message should be send.

### Send message
With a POST-Request to */messenger/chats*:
```
{
    "userid": <str>,
    "messenger": <str>,
    "message": <str>
}
```
a message can be sent.
When the sending was successful:
```
{
    "msg": "Successfully send message"
}
```

### Get all chats
A GET-Request to */messenger/chats*:
```
{
    "messenger": <str>
}
```
will give all open chats in the corresponding messenger
The Response will have following structure.
```
{
    "chats": [
        {
            "messages": [
                {
                    "author": <str>,
                    "message_id": <str>,
                    "messenger": <str>,
                    "text": <str>,
                    "timestamp": <double>
                },
                ...
            ]
            "title": <str>,
            "userid": <str>
        },
        ...
    ]
}
```

### Messages from single User
To GET the chats from one user:
```
{
    "messenger": <str>,
    "userid": <str>
}
```

The Response looks like following:
```
{
    "messages": [
        {
            "author": <str>,
            "message_id": <str>,
            "messenger": <str>,
            "text": <str>,
            "timestamp": <double>
        },
        ...
    ]
    "title": <str>,
    "userid": <str>
}
```

In the case the userid isn't registered:
```
{
    "error_msg": "Error while loading chat"
}
```

### Send a Message
To send a Message a POST-Requeset to */messenger/chats* in the form is required:
```
{
    "messenger": <str>,
    "userid": <str>,
    "message": <str>
}
```

### Profiles
The endpoint */messenger/profiles* takes the two parameters.
- **messenger**: String, Gives the messenger
- **userid**: String, optional. This Parameter is used if a sepecific Profile should be loaded

### All Profiles
To get all profiles, send the following GET-Request. 
```
{
    "messenger": <str>
}
```

The facebook messenger gives folloeing Response:
```
{
    "profiles":
    [
        {
            "userid": <str>,
            "name": <str>,
            "profile_url": <str>,
            "profile_picture_uri": <str>,
            "messenger": <str>
        },
        ...
    ]
}
```

With telegram messenger the Response looks like:
```
{
    "profiles":
    [
        {
            "userid": <str>,
            "name": <str>,
            "number": <str>,
            "messenger": <str>
        },
        ...
    ]
}
```

### Single Profile
If a Single Profile should be recieved a GET-Request is send:
```
{
    "messenger": <str>,
    "userid": <str>
}
```

The Response is similiar when recieving all Profiles. But it's not a list of profiles.

### Notification
The endpoint */stream* is used to send Notifications. A notfication will be recieved when:
- Message was succesful delivered
- Communication partner is typing
- Communication partner is active
- A message was read
- A new message recieved

If a message was read the following notification will be recieved:
```
{
    "chatid": <str>,
    "event": <str>,
    "message_id": <str>,
    "messenger": <str>
}
```

When a new message is available:
```
{
    "author": <str>,
    "event": <str>,
    "message": 
    {
        "author": <str>,
        "message_id": <str>,
        "messenger": <str>,
        "text": <str>,
        "timestamp": <str>
    },
    "messenger": <str>
}
```
