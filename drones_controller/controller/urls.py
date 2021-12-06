from django.urls import include, path
from rest_framework import routers
from .views import *



urlpatterns = [
    path('drones/', DroneViewSet.as_view()),
    path('drones/<int:serial_number>', DroneViewSet.as_view()),
    path('medications/', MedicationViewSet.as_view()),
    path('medications/<code>', MedicationViewSet.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
