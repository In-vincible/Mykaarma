from django.conf.urls import url, include
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.contrib import admin
from .views import *

app_name='endpoints'

urlpatterns = [
	url(r'^', index, name='index'),
	url(r'^location/$', get_dealer, name= 'location'),
	url(r'^login/', sign_in, name='signIn'),
	url(r'^signup/', sign_up, name='signup')

]