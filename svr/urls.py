from django.urls import path

from . import views

app_name = 'svr'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:svr_id>/', views.detail, name='detail'),
    path('add/', views.add, name='add'),
    path('<int:svr_id>/results/', views.results, name='results'),
]