from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HorarioFlexibleViewSet, HorariosExcepcionAPIView


router = DefaultRouter()
router.register(r'horarios', HorarioFlexibleViewSet, basename='horarios')

urlpatterns = [
    path('', include(router.urls)),
    path('horario/excepciones/', HorariosExcepcionAPIView.as_view(), name='horarios-excepcion'),
]
