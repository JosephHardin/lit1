from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class LitExplorerView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'litexplorer.html', context=None)
