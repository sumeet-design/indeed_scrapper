from django.urls import path
from . import views

urlpatterns = [
    # Define URL patterns for your views
    path('scrape/', views.scrape_and_store_data, name='scrape_data'),
    # Add more URL patterns as needed for other views
]
