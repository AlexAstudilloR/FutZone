from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AppointmentViewSet,
    ReservasPorFechaAPIView,
    DailyReservationSummaryAPIView,
    TimeSlotAvailabilityAPIView,
    FieldReservationSummaryAPIView,
    ExportReservationReportAPIView,
    ReservationStatusCountAPIView, 
)

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointments')

urlpatterns = [
    path('', include(router.urls)),

    path('reservas/fecha/', ReservasPorFechaAPIView.as_view(), name='reservas-fecha'),


    path('summary/', DailyReservationSummaryAPIView.as_view(), name='daily-reservation-summary'),
    path('summary/by-field/', FieldReservationSummaryAPIView.as_view(), name='summary-by-field'),
    path('summary/status-count/', ReservationStatusCountAPIView.as_view(), name='summary-status-count'),

    path('reservations/slots/', TimeSlotAvailabilityAPIView.as_view(), name='reservation-slots'),


    path('export/reservations/', ExportReservationReportAPIView.as_view(), name='export-reservations-report'),
]
