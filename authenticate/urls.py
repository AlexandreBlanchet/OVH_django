from django.conf.urls import url
from .views import SignUpView, login
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    url(r'^$', login, name="login"),
    url(r'^login$', LoginView.as_view(template_name="authenticate/login_form.html"), name="authenticate_login"),
    url(r'^logout$', LogoutView.as_view(), name="authenticate_logout"),
    url(r'signup$', SignUpView.as_view(), name="authenticate_signup"),
]
