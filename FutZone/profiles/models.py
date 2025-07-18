from django.db import models
import uuid
class ProfileModel(models.Model):
     id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,  
        editable=False
    )
     full_name = models.TextField(null=True, blank=True)
     cell_phone = models.TextField(null=True, blank=True)
     status = models.BooleanField(default=True, null=True)
     payment_qr= models.ImageField(upload_to='payment_method/',blank= True, null= True)
     is_admin= models.BooleanField(default=False,null=True)
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


     def __str__(self):
        return self.full_name or str(self.id)
     @property
     def is_authenticated(self):
        return True