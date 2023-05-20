from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('snacks/', views.snacks, name='snacks'),
    path('drinks/', views.drinks, name='drinks'),
    path('special/', views.special, name='special'),
]