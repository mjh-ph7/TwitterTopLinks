from django.db import models

class SessionData(models.Model):
	session_key = models.CharField(max_length=200)
	session_secret = models.CharField(max_length=200)
	screen_name = models.CharField(max_length=100)
	user_name = models.CharField(max_length=100)

	class Meta:
		unique_together = (("session_key", "session_secret", "screen_name"),)

	def __str__(self):
		return self.session_key,self.session_secret,self.screen_name,self.user_name

class TweetTable(models.Model):
	tweet_id = models.CharField(max_length=100, primary_key=True)
	timeline_screen_name = models.CharField(max_length=100)
	tweet_text = models.CharField(max_length=1000)
	tweet_entities = models.CharField(max_length=10000)
	tweet_screen_name = models.CharField(max_length=100)
	tweet_user_name = models.CharField(max_length=100)

	def __str__(self):
		return self.tweet_id,self.tweet_data
