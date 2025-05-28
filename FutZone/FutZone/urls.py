
from django.contrib import admin
from django.urls import path,include
import cancha.urls
import profiles.urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(cancha.urls)),
    path("api/auth/", include(profiles.urls))
]
