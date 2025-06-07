from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from profiles.authentication import SupabaseRemoteAuth
from profiles.permissions import IsAdminOrReadOnly
from .models import SoccerField
from .serializer import FieldSerializer
#from rest_framework.permissions import AllowAny        #Probar filtro 


class FieldViewSet(viewsets.ModelViewSet):
    queryset= SoccerField.objects.all()
    serializer_class= FieldSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    authentication_classes = [SupabaseRemoteAuth]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        available = self.request.query_params.get('available')

        if available is not None:
            if available.lower() == 'true':
                queryset = queryset.filter(available=True)
            elif available.lower() == 'false':
                queryset = queryset.filter(available=False)
        return queryset