from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from inmagik_utils.views import LoginRequiredMixin, AjaxableResponseMixin

class IndexView(TemplateView):
    template_name = "index.html"

"""
class UserFilesView(LoginRequiredMixin, TemplateView):
    template_name = "userfiles.html"
"""



class JoinWidgetView(LoginRequiredMixin, TemplateView):
    template_name = "ui/join_widget.html"

