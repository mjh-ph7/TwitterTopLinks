import http.client
import tweepy
from .models import SessionData, TweetTable
from .utils import * 
from django.contrib.auth import logout
from django.http import *
from django.shortcuts import render
from django.conf.urls import reverse


# login page
def main(request):
	if check_key(request):
		return HttpResponseRedirect(reverse('info')) #if authorized go to info
	else:
		return render(request, 'login.html') #else go to login

#if logout, remove session data
def unauth(request):
	if check_key(request):
		api = get_api(request)
		request.session.clear()
		logout(request)
	return HttpResponseRedirect(reverse('main')) #go to main

#display user info and store tweets in DB
def info(request):
	if check_key(request):
		api = get_api(request)
		access_key = request.session['access_key_tw']
		access_secret = request.session['access_secret_tw']
		user_data = api.me()
		store_session_info(request, access_key, access_secret, user_data)
		timeline_tweets = api.home_timeline() #get home timeline tweets
		store_tweet_data(request, timeline_tweets,user_data.screen_name)
		return render(request, 'info.html', {'user' : user_data})
	else:
		return HttpResponseRedirect(reverse('main'))

# tweepy OAuth
def auth(request):
	oauth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
	# direct the user to the authentication url, if logged-in and authorized go to callback url
	auth_url = oauth.get_authorization_url(True)
	response = HttpResponseRedirect(auth_url)
	# store the request token
	request.session['request_token'] = oauth.request_token
	return response

#callback url after authorization
def callback(request):
	verifier = request.GET.get('oauth_verifier')
	oauth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
	token = request.session.get('request_token')
	# remove the request token now we don't need it
	request.session.delete('request_token')
	oauth.request_token = token
	# get the access token and store
	try:
		oauth.get_access_token(verifier)
	except tweepy.TweepError:
		print('Error, failed to get access token')

	request.session['access_key_tw'] = oauth.access_token
	request.session['access_secret_tw'] = oauth.access_token_secret
	response = HttpResponseRedirect(reverse('info'))
	return response

#read tweet from home_timeline
def home_timeline(request):
	if check_key(request):
		api = get_api(request) #Oauth user
		screen_name = api.me().screen_name
		tweets_with_url = find_tweets_with_urls(request, screen_name)
		return render(request, 'timeline_tweets.html', {'timeline_tweets': tweets_with_url})
	else:
		return render(request, 'login.html') #goto login

#top users
def top_users(request):
	if check_key(request):
		api = get_api(request) #Oauth user
		screen_name = api.me().screen_name
		users_list = find_users_with_url_count(request, screen_name)
		return render(request, 'top_users.html', {'top_users': users_list})
	else:
		return render(request, 'login.html') #goto login

#top domains
def top_domains(request):
	if check_key(request):
		api = get_api(request) #Oauth user
		screen_name = api.me().screen_name
		domain_list = find_domain_hits(request, screen_name)
		return render(request, 'top_domains.html', {'top_domains': domain_list})
	else:
		return render(request, 'login.html') #goto login	

