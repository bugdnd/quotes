from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_quote, name='add_quote'),
    path('popular/', views.popular_quotes, name='popular_quotes'),
    path('vote/<int:quote_id>/', views.vote, name='vote'),
]


