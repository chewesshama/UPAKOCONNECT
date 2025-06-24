from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView
from .forms import RegistrationForm, LoginForm
from apps.users.models import CustomUser
from django.http import JsonResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from mtaa import tanzania



class CustomUserLoginView(LoginView):
    template_name = 'ariseclinic/accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True
    def get_success_url(self):
        return reverse_lazy("ariseclinic:index")


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('core:landing')


def get_districts(request):
    region = request.GET.get('region')
    if region:
        try:
            region_data = tanzania.get(region) if '-' in region else getattr(tanzania, region)
            districts = list(region_data.districts)
            return JsonResponse({'districts': districts})
        except AttributeError:
            return JsonResponse({'districts': []})
    return JsonResponse({'districts': []})

def get_wards(request):
    region = request.GET.get('region')
    district = request.GET.get('district')
    if region and district:
        try:
            region_data = tanzania.get(region) if '-' in region else getattr(tanzania, region)
            district_data = region_data.districts.get(district) if '-' in district else getattr(region_data.districts, district)
            wards = list(district_data.wards)
            return JsonResponse({'wards': wards})
        except AttributeError:
            return JsonResponse({'wards': []})
    return JsonResponse({'wards': []})

class UserCreationView(CreateView):
    form_class = RegistrationForm
    template_name = "ariseclinic/accounts/register.html"
    success_url = reverse_lazy('ariseclinic:index')

    def form_valid(self, form):
        messages.success(self.request, "User registered successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)


class UserProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'ariseclinic/home/profile.html'
    context_object_name = 'profile_user'
    
    def get_object(self):
        return self.request.user
class IndexView(LoginRequiredMixin ,TemplateView):
    template_name = "ariseclinic/home/index.html"


class TablesDisplayView(TemplateView):
    template_name = "ariseclinic/home/tables.html"
    


class IconsTemplateView(TemplateView):
    template_name = "ariseclinic/home/icons.html"
    
    
class ProfileDisplayView(TemplateView):
    template_name = "ariseclinic/home/profile.html"


class MapDisplayView(TemplateView):
    template_name = "ariseclinic/home/map.html"

