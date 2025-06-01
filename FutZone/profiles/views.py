from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ProfileModel
from .serializer import ProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from datetime import datetime
from pytz import UTC
import dotenv
import os
dotenv.load_dotenv()



SUPABASE_URL= os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY= os.getenv("SUPABASE_SERVICE_ROLE_KEY")



class ProfileViewSet(viewsets.ModelViewSet):
    queryset = ProfileModel.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]  # Cambia por tu permiso personalizado para validar Supabase JWT

    def get_queryset(self):
        # Opcional: filtrar para que cada usuario solo vea su perfil
        user_id = self.request.user.id  # O donde guardes el id al validar token
        return ProfileModel.objects.filter(id=user_id)

    def perform_create(self, serializer):
        # Asignar id del usuario autenticado (que viene del token)
        serializer.save(id=self.request.user.id)

class RegisterView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        full_name = request.data.get("full_name")
        cell_phone = request.data.get("cell_phone")
        birth_date = request.data.get("birth_date")

        if not email or not password:
            return Response({"error": "Email y password son requeridos."}, status=400)

        # Crear usuario en Supabase Auth
        res = requests.post(
            f"{SUPABASE_URL}/auth/v1/signup",
            json={"email": email, "password": password},
            headers={
                "apikey": SUPABASE_SERVICE_ROLE_KEY,
                "Content-Type": "application/json",
            }
        )

        if res.status_code != 200:
            return Response(res.json(), status=res.status_code)

        user = res.json().get("user")
        if not user or "id" not in user:
            return Response({"error": "No se recibió el ID del usuario."}, status=500)

        user_id = user["id"]

        try:
            ProfileModel.objects.create(
                id=user_id,
                full_name=full_name,
                cell_phone=cell_phone,
                birth_date=birth_date,
                created_at=datetime.now(UTC),
            )
        except Exception as e:
            return Response({"error": f"Error al crear perfil: {str(e)}"}, status=500)

        return Response({"message": "Usuario y perfil creados correctamente"}, status=201)