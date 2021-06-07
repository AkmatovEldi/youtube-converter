from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_by_link, name='redirect_by_link'),
    path('history/', views.get_history, name='get_history'),
    path('history/<int:history_id>/', views.get_history_details, name='get_history_details'),

]

