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


class RegisterView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'register.html', context=None)

    ####https://docs.djangoproject.com/en/4.2/topics/forms/
    def get_name(request):
        # if this is a POST request we need to process the form data
        if request.method == "POST":
            # create a form instance and populate it with data from the request:
            form = NameForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
                return HttpResponseRedirect("/thanks/")

        # if a GET (or any other method) we'll create a blank form
        else:
            form = NameForm()

        return render(request, "name.html", {"form": form})