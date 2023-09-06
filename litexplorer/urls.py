
from django.conf.urls.static import static
from django.urls import path
from litexplorer import views

urlpatterns = [
    path('', views.LitExplorerView.as_view()),
    path('idsubmit/', views.get_id),
    path('<int:noid>/', views.LitExplorerView.as_view()),
]
