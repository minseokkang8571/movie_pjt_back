from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.movie_list),
    path('<int:movie_pk>/', views.detail),
    path('api/', views.api),
    path('survey/', views.survey),
    path('boxoffice/', views.boxoffice),
    path('<int:movie_pk>/like/', views.like),
    path('random/', views.random_movie),
]
