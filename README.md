# LiveLobby

LiveLobby is a matchmaking system implemented in the form of a Django web application.

# Building 
Run the following commands to deploy the django application locally:

```sh
$ git clone https://github.com/mrpresidentjk/livelobby.git
$ cd livelobby
$ mkvirtualenv --python=python3 livelobby
$ pip install -r requirements.txt 
$ ./manage.py migrate
$ ./manage.py runserver
```

# Live Test Environment
The project is currently being hosted on heroku and can be accessed [here](https://livelobby.herokuapp.com/).
Code pushed to the master branch is automatically deployed this environment.

# Licensing
This project is MIT licensed and is open source.
