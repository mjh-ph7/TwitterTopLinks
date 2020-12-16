from django.test import TestCase
from .models import SessionData, TweetTable

#test models
class SessionDataTestCase(TestCase):
    def setUp(self):
        SessionData.objects.create(session_key="yyyyyy", session_secret="wwwww", screen_name="scrname1", user_name="name1")
        SessionData.objects.create(session_key="zzzzzz", session_secret="eeeee", screen_name="scrname2", user_name="name2")

    def test_model_sessiondata(self):
        ss1 = SessionData.objects.get(user_name="name1")
        ss2 = SessionData.objects.get(screen_name="scrname2")
        self.assertEqual(ss1.session_key, "yyyyyy")
        self.assertEqual(ss2.session_secret, "eeeee")

class TweetTableTestCase(TestCase):
    def setUp(self):
        TweetTable.objects.create(tweet_id=23, timeline_screen_name="scrname1", tweet_text="xyz", tweet_entities="hbhd",\
        tweet_screen_name="scrname2", tweet_user_name="name2")
        TweetTable.objects.create(tweet_id=92, timeline_screen_name="scrname2", tweet_text="abc", tweet_entities="enbfg",\
        tweet_screen_name="scrname1", tweet_user_name="name1")

    def test_model_tweettable(self):
        tw1 = TweetTable.objects.get(tweet_user_name="name1")
        tw2 = TweetTable.objects.get(tweet_screen_name="scrname2")
        self.assertEqual(tw1.timeline_screen_name, "scrname2")
        self.assertEqual(tw2.tweet_id, 23)

#TODO