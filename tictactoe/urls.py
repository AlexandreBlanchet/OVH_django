from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView

from .views import home, welcome, new_invitation, accept_invitation, game_detail, make_move, AllGamesList

urlpatterns = [
    url(r'^home$', home, name="tictactoe_home"),
    url(r'^$', welcome, name="tictactoe_welcome"),
    url(r'^new_invitation$', new_invitation, name="tictactoe_new_invitation"),
    url(r'accept_invitation/(?P<id>\d+)/$', accept_invitation, name="tictactoe_accept_invitation"),
    url(r'detail/(?P<id>\d+)/$', game_detail, name="tictactoe_detail"),
    url(r'make_move/(?P<id>\d+)/$', make_move, name="tictactoe_make_move"),
    url(r'all$', AllGamesList.as_view()),
]