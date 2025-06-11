from django.urls import path,include
from .views import FieldViewSet
from rest_framework.routers import DefaultRouter


router= DefaultRouter()
router.register(r'canchas',FieldViewSet)


urlpatterns = [
    path('', include(router.urls)),  
]