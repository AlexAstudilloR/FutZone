from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, ProfileViewSet, MyProfileView

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('mi-perfil/', MyProfileView.as_view(), name='mi-perfil'),
    path('', include(router.urls)),
    

]
