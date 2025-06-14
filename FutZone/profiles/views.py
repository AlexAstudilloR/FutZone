from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from pytz import UTC
import requests
import os
import dotenv

from .models import ProfileModel
from .serializer import ProfileSerializer

dotenv.load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")


def validate_registration_data(data):
    required_fields = ["email", "password", "full_name"]
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return False, {"error": f"Faltan campos requeridos: {', '.join(missing)}"}
    return True, None


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = ProfileModel.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.user.id
        return ProfileModel.objects.filter(id=user_id)

    def perform_create(self, serializer):
        serializer.save(id=self.request.user.id)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        is_valid, errors = validate_registration_data(request.data)
        if not is_valid:
            return Response(errors, status=400)

        email = request.data["email"]
        password = request.data["password"]
        full_name = request.data.get("full_name")
        cell_phone = request.data.get("cell_phone")

        res = requests.post(
            f"{SUPABASE_URL}/auth/v1/admin/users",
            json={
                "email": email,
                "password": password,
                "email_confirm": True,
                "user_metadata": {
                    "full_name": full_name,
                    "cell_phone": cell_phone,
                },
            },
            headers={
                "apikey": SUPABASE_SERVICE_ROLE_KEY,
                "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
                "Content-Type": "application/json",
            },
        )

        if res.status_code != 200:
            return Response(res.json(), status=res.status_code)

        user = res.json()
        user_id = user.get("id")

        if not user_id:
            return Response({"error": "No se recibió el ID del usuario."}, status=500)

        try:
            ProfileModel.objects.create(
                id=user_id,
                full_name=full_name,
                cell_phone=cell_phone,
                created_at=datetime.now(UTC),
            )
        except Exception:

            requests.delete(
                f"{SUPABASE_URL}/auth/v1/admin/users/{user_id}",
                headers={
                    "apikey": SUPABASE_SERVICE_ROLE_KEY,
                    "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
                },
            )
            return Response({"error": "Error al crear perfil. Usuario eliminado."}, status=500)

        return Response({"message": "Usuario y perfil creados correctamente"}, status=201)
class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user  
        return Response({
            "id": profile.id,
            "full_name": profile.full_name,
            "cell_phone": profile.cell_phone,
            "is_admin": profile.is_admin,
        })