from django.conf.urls import url
from django.conf.urls.static import static
from litexplorer import views

urlpatterns = [
    url(r'^$', views.LitExplorerView.as_view()),
]
