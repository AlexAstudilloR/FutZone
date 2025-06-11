from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WeeklyScheduleViewSet,
    DateExceptionViewSet,
    DateExceptionByDateAPIView,
)

router = DefaultRouter()
router.register(r'weekly-schedules', WeeklyScheduleViewSet, basename='weekly-schedules')
router.register(r'date-exceptions',  DateExceptionViewSet,  basename='date-exceptions')

urlpatterns = [
    path('', include(router.urls)),
    path('exceptions/', DateExceptionByDateAPIView.as_view(), name='exceptions-by-date'),
    
]
