from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class IndexView(LoginRequiredMixin ,TemplateView):
    template_name = "ariseclinic/home/index.html"
    

class TablesDisplayView(TemplateView):
    template_name = "ariseclinic/home/tables.html"