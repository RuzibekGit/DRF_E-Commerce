from django.urls import path
from .views import ScrapeReceiptView

urlpatterns = [
    path('receipt/', ScrapeReceiptView.as_view(), name='scrape-receipt'),
]
