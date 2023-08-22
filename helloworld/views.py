 # helloworld/views.py
from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'home.html', context=None)

class LoginView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'login.html', context=None)