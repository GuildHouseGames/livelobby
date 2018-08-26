# LiveLobby

LiveLobby is a matchmaking system implemented in the form of a Django web application.

# Building 
Run the following commands to deploy the django application locally:

```sh
$ git clone https://github.com/mrpresidentjk/livelobby.git
$ cd livelobby
$ git checkout develop
$ pipenv install
$ pipenv shell
$ cd livelobby/settings/ 
$ ln -s development.py __init__.py
$ cd ../../
$ ./manage.py migrate
$ ./manage.py runserver
```

# Live Test Environment
The project is currently being hosted on heroku and can be accessed [here](https://livelobby.herokuapp.com/events).
Code pushed to the master branch is automatically deployed this environment.

# Licensing
This project is MIT licensed and is open source.
