from django.conf.urls import url
from . import consumers

websocket_urlpatterns = [
    url(r'ws/castlemaze/game/(?P<game_id>\d+)/$', consumers.GameConsumer),
]