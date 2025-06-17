from django.urls import path
from .views import CustomUserLoginView, logout_view, UserRegisterView

app_name = 'users'

urlpatterns = [
    path('login/', CustomUserLoginView.as_view(), name='login'),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("logout/", logout_view, name="logout"),
]
