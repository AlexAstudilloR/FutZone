from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet,ReservasPorFechaAPIView,DailyReservationSummaryAPIView
from django.urls import path, include

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointments')

urlpatterns = [
    path('', include(router.urls)),
    path('reservas/fecha/', ReservasPorFechaAPIView.as_view(), name='reservas-fecha'),
    path('summary/', DailyReservationSummaryAPIView.as_view(), name='daily-reservation-summary'),
]
