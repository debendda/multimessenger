# README #

# Introduction

This is the documentation for the project multi-messenger for the lecture system administartion. This project provides an api written in pyhton for the messengers Telegram and Facebook messenger.

**This is just an example and should not be hosted online.**
**We are not liable for any damage incurred.**

# Setup
In order to setup this API you have to pull this repository with ```git clone https://github.com/debendda/multimessenger.git```.
If the pull was successful you can navigate to the setup folder and execute this command ```chmod u+x setup.py && python setup.py```.

This installation Script will install all the dependencies, creates the Database and gives you the possibility to create a new User.

It's recommended to navigate to the /src folder and change the value of ```app.config['SECRET_KEY']``` and ```app.config['JWT_SECRET_KEY']``` field in the app.py file.

Also in *multimessenger/src/messengers/telegram_messenger/telegram_messenger.py*, you should change the *database_encryption_key*.

![grafik](https://user-images.githubusercontent.com/33962621/121920260-29517900-cd38-11eb-8782-70e8d34a8b5c.png)

By default the Database from Telegram is saved under */tmp/phone_number/*, which means that the Chats are deleted every time you restart your Computer. To change the path where the Database is stored you can modify that by adding ```library_path = *your_path*``` to the Telegram Object. 

Since this Project uses HTTPS you'll need a Certificate. You can create your own unsigned Certificate and put it in the folder *multimessenger/key/*.

# Usage
To start the server, navigate to *multimessenger/src* 
