from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  HorarioDisponibleViewSet, HorariosFiltradosAPIView

router = DefaultRouter()

router.register(r'horarios', HorarioDisponibleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('filtrados/', HorariosFiltradosAPIView.as_view(), name='horarios-filtrados'),
]
