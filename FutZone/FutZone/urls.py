
from django.contrib import admin
from django.urls import path,include
import cancha.urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(cancha.urls))
]
