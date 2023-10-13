from django.urls import path
from .views import *

urlpatterns = [
    path('', stockPageView, name= 'stock')
]