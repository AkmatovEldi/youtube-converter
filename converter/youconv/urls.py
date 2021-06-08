from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_by_link, name='redirect-by-link'),
    path('history/', views.get_history, name='get-history'),
    path('history/<int:history_id>/', views.get_history_details, name='get-history-details'),

]

