# Endpoint description

## API

#### Logout
##### Logout Access
Not valid access token
```
{
    "msg": "Token has expired"
}
```

Successfull logout access

```
{
    "msg": "Access token has been revoked"
}
```



## Chats

#### Get all Chats

Endpoint
```
jwt_required
GET /messenger/chats - Return all Chats
```
Request from client
```
Request
{
    "messenger" : <str>
}
```

Response
```
Response 
{ 
    'chats':
        [ 
            {
                "userid" : <int>
                "messages" : 
                [
                    {
                        "messenger" : <str>,
                        "text" : <str>,
                        "timestamp" : <int>,
                        "author" : <str>
                    },
                    ...
                ]
            }
        ]
}
```

#### Get the chat from specific user and messenger 

Endpoint
```
jwt_required
GET /messenger/chats - Return chat from user with given userid
```
Request from client
```
Request
{
    "messenger" : <str>
    "userid" : <int>
}
```
Response
```
Respons 
{ 
    "userid" : <int>
    "messages" : 
    [
        {
            "messenger" : <str>,
            "text" : <str>,
            "timestamp" : <int>,
            "author" : <str>
        },
        ...
    ]
}
```
#### Send message to specific user and messenger
Endpoint
```
jwt_required
POST /messenger/chats : Send message to given userid and messenger
```
Request from client
```
Request
{
    "userid" : <int>,
    "messenger" : <str>,
    "message" : <str>
}
```
Response
```
Respons
{
    "message" : "Successfully send message." | "Error while sending message"
}
```

## Profiles

#### Get all profile infos

Endpoint
```
jwt_required
GET /messenger/profiles : alle profile zurückgeben
```
Request from client
```
Request
{
    "messenger" : <str>
}
```
Response
```
Response 
{ 
    'profiles':
        [ 
            {
                "userid" : <int>
                "name": <str>,
                "handy_number": <str>,
                "email" : <str>,
                "profile_url" : <str> 
                "profile_picture_uri" : <str>,
                "messenger" : 
                    [
                        <str>
                    ]
            }
        ]
}
```

#### Get specific profile info
Endpoint
```
jwt_required
GET /messenger/profiles
```
Request from client
```
{
    "messenger" : <str>,
    "userid" : <int>
}
```
Response
```
Respons     
{
    "userid" : <int>
    "name": <str>,
    "handy_number": <str>,
    "email" : <str>,
    "profile_picture_uri" : <str>,
    "messenger" : 
    [
        <str>
    ]
}
```

## Notifications

#### New Message

```
GET /messenger/notifications - Stream

Response
{
    "event" : "message" | "read" | ...
    "author" : <int>,
    "message" : 
    {
        "messenger" : <str>,
        "text" : <str>,
        "timestamp" : <int>,
        "author" : <str>
    }
}

```

## Login or authentification for messengers

### Login

```
jwt_required
POST /messenger/login 
```

### Facebook Messenger
#### Login with password
Request client
```
Request
{
    "messenger" : "facebook_messenger",
    "email" : <str>,
    "password" : <str>
}
```
Response
```
Response
{
    "messenger" : "facebook_messenger",
    "msg" : "Success."
}
```
#### Login with cookie (Fällt vermutlich raus)
Request client
```
Request
{
    "messenger" : "facebook",
    "cookie" : <str>
}
```
Respose
```
Response
{
    "messenger" : "facebook",
    "message" : "Successfully logged in." | "Error while login"
}
```
#### Whatsapp
???
```
Request (Whatsapp)
{
    "messenger" : "whatsapp"
}

Response
{
    "qr_code" : code
    "expires"??? 
}

Nach respose???
QR-Code muss gescannt werden, evtl hidden link zurückschicken anstatt QR-Code?
Evtl success im Stream mitteilen? Evtl Client muss GET auf "messengers/authenticate/success" machen um zu schauen ob es geklappt hat.
```

### Logout 

```
jwt_required
POST /messenger/logout
```

### Facebook
#### Logout

Request from Client

```
Request
{
    "messenger" : "facebook_messenger"
}
```
Response
```
{
    "messenger" : "facebook_messenger",
    "msg" : "Success"
}
```

```
{
    "error_msg" : "Error while logging in to facebook messenger."
}
```
