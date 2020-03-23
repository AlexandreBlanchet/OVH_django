# Talk urls
from django.conf.urls import  url
from .views import create_post, home


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^create_post/$', create_post, name='create_post'),
]