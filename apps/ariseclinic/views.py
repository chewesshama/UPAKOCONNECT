from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class IndexView(LoginRequiredMixin ,TemplateView):
    template_name = "ariseclinic/home/index.html"
    

#class ClinicLoginView(TemplateView):
#    template_name = 'ariseclinic/accounts/login.html'
    


#class ClinicRegisterView(TemplateView):
#    template_name = 'ariseclinic/accounts/register.html'
    

