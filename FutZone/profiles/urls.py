from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, ProfileViewSet, MyProfileView,AdminPaymentQRView, LastPaymentQRView

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('mi-perfil/', MyProfileView.as_view(), name='mi-perfil'),
    path('payment-method/', AdminPaymentQRView.as_view(), name='payment-method'),
    path('payment-method/last/', LastPaymentQRView.as_view(), name='last-payment-method'),
    path('', include(router.urls)),
    

]
