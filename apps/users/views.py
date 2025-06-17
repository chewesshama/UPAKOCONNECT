from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm, CustomUserCreationForm
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from .models import CustomUser



def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('core:landing')  # or wherever you redirect after logout


class CustomUserLoginView(LoginView):
    template_name = 'ariseclinic/accounts/login.html'
    authentication_form = CustomLoginForm
    redirect_authenticated_user = True


class UserRegisterView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'ariseclinic/accounts/register.html'
    success_url = reverse_lazy('users:login')
    success_message = "Account created successfully! You can now login."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['msg'] = ''
        context['success'] = False
        return context
