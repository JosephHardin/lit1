from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpRequest

import litexplorer.litexplorer
from .forms import IdForm
# Create your views here.
class LitExplorerView(TemplateView):
    template_name = "litexplorer.html"
    def get(self, request, **kwargs):
        print("I AM HEAR AND KWARGS IS")
        if 'errormessage' in kwargs:
            print("errormessage equals " + kwargs.get("errormessage"))
        else:
            print(kwargs)
        print("And get is ")
        print(request.GET)
        context = {}
        context['noid'] = int(request.GET.get('noid', 0))
        print(context)
        return render(request, 'litexplorer.html', context=context)









def get_id(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = IdForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            litexplorer.litexplorer.start(form['id'].value())
            return HttpResponseRedirect("/register/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = IdForm()


    return HttpResponseRedirect("/litexplorer/?noid=1")