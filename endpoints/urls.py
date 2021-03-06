from django.conf.urls import url, include
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.contrib import admin
from .views import *

app_name='endpoints'

urlpatterns = [
	url(r'^location/$', get_dealer, name= 'location'),
	url(r'^login/$', sign_in, name='signIn'),
	url(r'^signup/$', sign_up, name='signup'),
	url(r'^passChange/', reset_pass, name='password reset'),
	url(r'^logout/', sign_out, name = 'logout'),
	url(r'^mail/', send_email, name = 'mail'),
	url(r'^search/$', search_car, name='search'),
	url(r'^history/$', past_searches, name='history'),
	url(r'^$', index, name='index')
]