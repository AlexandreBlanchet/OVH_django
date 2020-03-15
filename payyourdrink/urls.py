from django.conf.urls import url
from .views import welcome, home, new_deal, change_deal

urlpatterns = [
    url(r'^$', welcome, name="payyourdrink_welcome"),
    url(r'^home$', home, name="payyourdrink_home"),
    url(r'^new_deal$', new_deal, name="payyourdrink_new_deal"),
    url(r'change_deal/(?P<id>\d+)/$', change_deal, name="payyourdrink_change_deal"),

]