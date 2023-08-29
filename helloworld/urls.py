# helloworld/urls.py
from django.urls import include, path
from django.conf.urls.static import static
from helloworld import views

urlpatterns = [
    path('', views.HomePageView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('new-user/', views.make_user, name="new-user"),



]
