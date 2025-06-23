from django.urls import path
from .views import IndexView, TablesDisplayView

app_name = "ariseclinic"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("tables/", TablesDisplayView.as_view(), name="tables"),
#    path("login/", ClinicLoginView.as_view(), name="login"),
#    path("register/", ClinicRegisterView.as_view(), name="register")
]
