from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from datetime import datetime
from pytz import UTC
import requests
import os
import dotenv
import re
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

    if len(data["password"]) < 6:
        return False, {"error": "La contraseña debe tener al menos 6 caracteres."}

    if "@" not in data["email"]:
        return False, {"error": "El correo no es válido."}

    full_name = data["full_name"]
    if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+", full_name):
        return False, {"error": "El nombre solo puede contener letras y espacios."}

    cell_phone = data.get("cell_phone", "")
    if cell_phone and not re.fullmatch(r"09\d{8}", cell_phone):
        return False, {"error": "El número de celular debe comenzar con 09 y tener 10 dígitos."}

    return True, None

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = ProfileModel.objects.filter(status=True).order_by('-created_at')
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        all_param = self.request.query_params.get("all", "false").lower() == "true"

        if user.is_admin:
            return ProfileModel.objects.all() if all_param else ProfileModel.objects.filter(status=True)
        return ProfileModel.objects.filter(id=user.id, status=True)

    def perform_create(self, serializer):
        user = self.request.user
        data = self.request.data
        requested_admin = str(data.get("is_admin", "false")).lower() == "true"

        if requested_admin and not user.is_admin:
            raise PermissionDenied("No tienes permisos para crear administradores.")

        # Admin puede asignar el ID de otro usuario
        if user.is_admin and "id" in data:
            serializer.save()
        else:
            # Usuario común crea su propio perfil sin admin
            serializer.save(id=user.id, is_admin=False)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = False  # 👈 Borrado lógico
        instance.save()
        return Response({"detail": "Perfil desactivado correctamente"}, status=status.HTTP_204_NO_CONTENT)
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
            error_msg = res.json().get("msg", "Error desconocido al registrar usuario.")

            traducciones = {
                "Password should be at least 6 characters": "La contraseña debe tener al menos 6 caracteres.",
                "User already registered": "Este correo ya está registrado.",
                "A user with this email address has already been registered": "Ya hay un usuario registrado con este correo"
            }

            error_traducido = traducciones.get(error_msg, error_msg)
            return Response({"error": error_traducido}, status=res.status_code)

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

            "full_name": profile.full_name,
            "cell_phone": profile.cell_phone,
            "is_admin": profile.is_admin,
        })
