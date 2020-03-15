from django.conf.urls import url
from .views import welcome, home, edit_note

urlpatterns = [
    url(r'^$', welcome, name="keepinmind_welcome"),
    url(r'^home$', home, name="keepinmind_home"),
    url(r'edit_note/(?P<id>\d+)/$', edit_note, name="keepinmind_edit_note"),
]