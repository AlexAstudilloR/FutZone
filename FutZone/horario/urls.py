from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HorarioFlexibleViewSet

router = DefaultRouter()
router.register(r'horarios', HorarioFlexibleViewSet, basename='horarios')

urlpatterns = [
    path('', include(router.urls))
]
