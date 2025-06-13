from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .forms import LoginForm, UserCreateForm

class UserLoginView(LoginView):
    template_name = "users/login.html"
    authentication_form = LoginForm

class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()
        return super().form_valid(form)
