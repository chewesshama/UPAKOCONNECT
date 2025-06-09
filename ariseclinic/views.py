from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "ariseclinic/index.html"
    
    
class LoginView(TemplateView):
    template_name = "ariseclinic/login.html"