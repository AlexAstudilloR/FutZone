from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from profiles.authentication import SupabaseRemoteAuth
from profiles.permissions import IsAdminOrReadOnly
from .models import SoccerField
from .serializer import FieldSerializer



class FieldViewSet(viewsets.ModelViewSet):
    queryset = SoccerField.objects.all().order_by('id')
    serializer_class = FieldSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    authentication_classes = [SupabaseRemoteAuth]

    def get_queryset(self):
        qs = super().get_queryset()
        available = self.request.query_params.get('available')
        if available is not None:
            val = True if available.lower() == 'true' else False
            qs = qs.filter(available=val)
        return qs
