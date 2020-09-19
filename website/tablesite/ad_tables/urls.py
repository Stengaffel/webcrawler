from django.urls import path

from . import views

urlpatterns = [
        path('', views.index, name='index'),

        # Path to the ads from indeed
        path('<str:table_name>/', views.createTable, name='indeed'),
        ]
