from django.conf.urls import url
from .views import welcome, home, game, action_request

urlpatterns = [
    url(r'^$', welcome, name="castlemaze_welcome"),
    url(r'^home$', home, name="castlemaze_home"),
    url(r'^game/(?P<id>\d+)', game, name="castlemaze_game"),
    url(r'action_request', action_request, name='castlemaze_action_request' ),
]