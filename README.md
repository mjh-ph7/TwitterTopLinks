# Twitter Top Links App

### Features

  - List user stream tweets
  - Show top domains shared
  - Show top sharers

#### Installation
Change directory to app folder


```
pip3 install django==1.8.1
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
Generate Twitter Credential from [Twitter Developer](https://developer.twitter.com/en), set the callback URLs in settings of Twitter Application to

http://127.0.0.1:8000/callback/

#### Tests
Change directory to app folder

```
python3 manage.py test
```

