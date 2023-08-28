from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from litexplorer import views

urlpatterns = [
    url(r'^$', views.LitExplorerView.as_view()),
    url(r'^idsubmit/', views.get_id),
]
