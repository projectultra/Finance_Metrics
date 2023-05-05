from django.urls import path
from . import views
from .Templates import Mainpage
urlpatterns = [
    path('', views.DisplayStocks.as_view(), name='display_stocks'),
]