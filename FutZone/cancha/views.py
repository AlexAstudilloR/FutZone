from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from profiles.authentication import SupabaseRemoteAuth
from profiles.permissions import IsAdminOrReadOnly
from .models import SoccerField
from .serializer import FieldSerializer


class FieldViewSet(viewsets.ModelViewSet):
    queryset= SoccerField.objects.all()
    serializer_class= FieldSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    authentication_classes = [SupabaseRemoteAuth]