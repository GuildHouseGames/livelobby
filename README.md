# LiveLobby

LiveLobby is a matchmaking system implemented in the form of a Django web application.

# Building 

Run the following commands to deploy the django application:

```sh
$ git clone https://github.com/mrpresidentjk/livelobby.git
$ cd livelobby
$ mkvirtualenv --python=python3 livelobby
$ pip install requirements.txt 
$ ./manage.py migrate
$ ./manage.py runserver
```

# Licensing
This library is MIT licensed and is open source.
