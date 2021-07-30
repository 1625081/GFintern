from django.urls import path

from . import views

app_name = 'compute'
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:compute_id>/', views.detail, name='detail'),
    # ex: /polls/add/
    path('add/', views.add, name='add'),
    # ex: /polls/5/results/
    path('<int:compute_id>/<int:cop_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:compute_id>/vote/', views.vote, name='vote'),
]