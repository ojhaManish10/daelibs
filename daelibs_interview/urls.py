# urls.py

from django.urls import path
from main import views

urlpatterns = [
    path('traffic/dayOfWeekAverageCount/', views.day_of_week_average_count),
]
