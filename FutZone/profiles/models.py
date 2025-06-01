from django.db import models
import uuid
class ProfileModel(models.Model):
     id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,  # En Supabase usas auth.uid(), aquí generamos UUID automáticamente
        editable=False
    )
     full_name = models.TextField(null=True, blank=True)
     cell_phone = models.TextField(null=True, blank=True)
     birth_date = models.DateField(null=True, blank=True)
     status = models.BooleanField(default=True, null=True)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

     class Meta:
        db_table = "profiles"
        managed = False  # <--- esta es la clave  # El nombre exacto de la tabla en Supabase

     def __str__(self):
        return self.full_name or str(self.id)
     @property
     def is_authenticated(self):
        return True