
from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^$', views.main, name='main'), 				
    url(r'^callback/$', views.callback, name='auth_return'), 	
    url(r'^logout/$', views.unauth, name='oauth_unauth'), 		
    url(r'^auth/$', views.auth, name='oauth_auth'), 		
    url(r'^info/$', views.info, name='info'), 				
    url(r'^home_timeline/$',views.home_timeline, name='home_timeline'),
    url(r'^top_users/$',views.top_users, name='top_users'),
    url(r'^top_domains/$',views.top_domains, name='top_domains'),
]
