from django.conf.urls import url
from .views import welcome, home

urlpatterns = [
    url(r'^$', welcome, name="keepinmind_welcome"),
    url(r'^home$', home, name="keepinmind_home"),
]