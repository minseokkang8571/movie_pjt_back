from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<int:article_pk>/', views.detail, name='detail'),
    path('<int:article_pk>/ud/', views.update_delete, name='update_delete'),
    path('<int:article_pk>/comment/create/', views.comment_create, name='comment_create'),
    path('<int:article_pk>/comment/<int:comment_pk>/', views.comment_ud, name='comment_rud'),
]
