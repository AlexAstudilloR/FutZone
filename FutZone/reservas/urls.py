from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet
from .views import ReservasPorFechaAPIView
from django.urls import path, include

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('reservas/fecha/', ReservasPorFechaAPIView.as_view(), name='reservas-fecha'),
]
