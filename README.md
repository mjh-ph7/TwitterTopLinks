# Twitter Top Links App

### Features

  - List user stream tweets
  - Show top domains shared
  - Show top sharers
  
Use the app [here](twitter-tl.herokuapp.com)

#### Installation
Change directory to app folder


```
pip3 install django==2.2.17
pip3 install tweepy
```
or
```
pip3 install -r requirements.txt
```

#### Set up App

Change directory to app folder

```
python3 manage.py makemigrations twitterapp
python3 manage.py migrate
python3 manage.py runserver
```

#### Callback URL
Generate Twitter Credential from [Twitter Developer](https://developer.twitter.com/en), set the callback URL in settings of Twitter Application to

http[s]://[app-url]/callback/

#### Tests
Change directory to app folder

```
python3 manage.py test
```

