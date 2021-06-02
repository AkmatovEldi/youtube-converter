from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_by_link, name='redirect_by_link'),
]