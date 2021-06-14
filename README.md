# README #

# Introduction

This is the documentation for the project multi-messenger for the lecture system administartion. This project provides an api written in pyhton for the messengers WhatsApp, Signal and Facebook messenger.

# Setup

## Virual Environment

```
sudo apt-get install virtualenv 
```

To create a new virtual environment you have to use:

```
virtualenv *path*
```

To activate the virtual environment you have to type the command:

```
cd multimessenger
source virt_env/bin/activate
```

To deactivate the virtual environment, you can type:

```
deactivate
```

## Flask
### Install Flask
To install Flask, you need to enable the virtual environment.
```
pip3 install Flask
```

### https for Flask
For https you need to install pyopenssl.

```
pip install pyopenssl
```

You have to create a self signed certificate:

```
cd multimessenger
mkdir key
cd key 
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```


### Start development server

```
cd src
python3 app.py
```

## Install SQLite3

```
sudo apt install sqlite3
```

## Install SQL-Alchemy
```
pip3 install flask-sqlalchemy
```

```
pip install flask-restful
```
```
pip install flask-jwt-extended

```

pip install -U flask-cors

## Install python-telegram
```
pip install python-telegram
```
In order to use this library you must provide an api_id and api_hash.
To get them, follow the steps on the telegram page. https://core.telegram.org/api/obtaining_api_id

This app checks if the api_id and api_hash are set in the enviroment.
To set them type in terminal: 
```
export TG_API_ID=your_api_id
export TG_API_HASH=your_api_hash
```
In order to avoid to supply the id/hash every time, add them to .bashrc.

Careful here, they're visible to everyone who has access to your .bashrc file.