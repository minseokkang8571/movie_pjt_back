from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile),
    path('survey/<int:genre_pk>/', views.set_genre)
]
