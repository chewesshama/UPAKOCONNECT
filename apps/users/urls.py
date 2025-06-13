from django.urls import path
from .views import UserLoginView, UserCreateView
from django.contrib.auth.views import LogoutView

app_name = "users"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("create/", UserCreateView.as_view(), name="create"),
    path("logout/", LogoutView.as_view(next_page="users:login"), name="logout"),
]
