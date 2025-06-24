from django.urls import path
from .views import IndexView, TablesDisplayView, IconsTemplateView, UserProfileView, MapDisplayView, UserCreationView, get_districts, get_wards, CustomUserLoginView, logout_view

app_name = "ariseclinic"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path('login/', CustomUserLoginView.as_view(), name='login'),
    path("logout/", logout_view, name="logout"),
    path("register/", UserCreationView.as_view(), name="register"),
    path("tables/", TablesDisplayView.as_view(), name="tables"),
    path("icons/", IconsTemplateView.as_view(), name="icons"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("map/", MapDisplayView.as_view(), name="map"),
    path("get_districts/", get_districts, name="get_districts"),
    path("get_wards/", get_wards, name="get_wards"),

]
