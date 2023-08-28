# helloworld/urls.py
from django.conf.urls import url
from django.conf.urls.static import static
from helloworld import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^login/', views.LoginView.as_view()),
    url(r'^register/', views.RegisterView.as_view()),
    url(r'^new-user/', views.make_user, name="new-user"),



]
