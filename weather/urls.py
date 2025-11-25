from django.urls import path
from .views import WeatherForecastView, LocationListCreateView, LocationDetailView

urlpatterns = [
    path("forecast/", WeatherForecastView.as_view(), name="weather_forecast"),
    path("locations/", LocationListCreateView.as_view(), name="locations_list"),
    path("locations/<int:pk>/", LocationDetailView.as_view(), name="locations_detail"),
]
