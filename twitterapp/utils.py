import json
import re
import tweepy
from .views import *
from .models import SessionData, TweetTable
from collections import OrderedDict
from urllib.parse import urlparse

API_KEY = 'LptFWHaXJ5wRIGy8tkgR2h8JS'
API_SECRET_KEY = 'E5UFVKQC8R2Nu1Y1RcoFytIZAaQyze5EByH9umT36hLmcXWRQR'

#check if auth key stored
def check_key(request):
	try:
		access_key = request.session.get('access_key_tw', None)
		if not access_key:
			return False
	except KeyError:
		return False
	return True

#get tweepy api 
def get_api(request):
	oauth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
	access_key = request.session['access_key_tw']
	access_secret = request.session['access_secret_tw']
	oauth.set_access_token(access_key, access_secret)
	api = tweepy.API(oauth)
	return api

#get domain name from url
def get_domain_name(url, remove_http=True):
    uri = urlparse(url)
    if remove_http:
        domain_name = f"{uri.netloc}"
    else:
        domain_name = f"{uri.netloc}://{uri.netloc}"
    return domain_name

#detect url in text
def find_urls_in_text(text):
	urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',\
	text) #regular expression to detect link in tweet text
	if len(urls) > 0:
		return True, len(urls)
	else:
		return False, 0

# find tweets which have at least one url link in it
def find_tweets_with_urls(request, current_screen_name):
	tweet_query = TweetTable.objects.filter(timeline_screen_name=current_screen_name)
	api = get_api(request)
	tweets_with_urls = []
	for tweet in tweet_query:
		url_present,_= find_urls_in_text(tweet.tweet_text)
		if url_present:
			url_tweet = api.get_oembed(tweet.tweet_id) #get embedded tweet
			tweets_with_urls.append(url_tweet['html'])
	return tweets_with_urls

#find no. of times domains shared
def find_domain_hits(request, screen_name):
	tweet_query = TweetTable.objects.filter(timeline_screen_name=screen_name)
	domain_dict = OrderedDict()  #dict for user hits

	for tweet in tweet_query:
		_,url_size = find_urls_in_text(tweet.tweet_text)
		if url_size>0:
			text = tweet.tweet_entities.replace("\'", "\"")
			tweet_entities = json.loads(text)
			for i in range(url_size):
				dom_name = tweet_entities['urls'][i]['expanded_url']
				dom_name = get_domain_name(dom_name)
				if dom_name in domain_dict:
					domain_dict[dom_name]+=1
				else:
					domain_dict[dom_name]=1
	domain_dict = dict(sorted(domain_dict.items(), key=lambda item: item[1]))
	return domain_dict

#find the no. of urls shared by users for a timeline
def find_users_with_url_count(request, screen_name):
	tweet_query = TweetTable.objects.filter(timeline_screen_name=screen_name)
	user_dict = OrderedDict()  #dict for user hits
	for tweet in tweet_query:
		_,url_size = find_urls_in_text(tweet.tweet_text)
		if url_size>0:
			if tweet.tweet_screen_name in user_dict:
				user_dict[tweet.tweet_screen_name]+=url_size
			else:
				user_dict[tweet.tweet_screen_name]=url_size
	user_dict = dict(sorted(user_dict.items(), key=lambda item: item[1]))
	return user_dict

#save session data
def store_session_info(request, access_key, access_secret, user_data):
	user_screen_name = user_data.screen_name
	user_name = user_data.name
	if not SessionData.objects.filter(session_secret=access_secret, \
		session_key=access_key).exists():
		db_row = SessionData(session_key=access_key, session_secret=access_secret,\
		screen_name=user_screen_name, user_name=user_name)
		db_row.save()

#save tweet data
def store_tweet_data(request, timeline_tweets, screen_name):
	for tweet in timeline_tweets:
		tweet_id_found = tweet.id
		if not TweetTable.objects.filter(tweet_id=tweet_id_found).exists():
			db_row = TweetTable(tweet_id=tweet_id_found, timeline_screen_name=screen_name,\
			tweet_text=tweet.text, tweet_entities=tweet.entities, \
			tweet_screen_name=tweet.user.screen_name, tweet_user_name=tweet.user.name)
			db_row.save()



