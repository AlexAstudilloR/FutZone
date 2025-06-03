from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
import cancha.urls
import profiles.urls
import reservas.urls
import horario.urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(cancha.urls)),
    path("api/auth/", include(profiles.urls)),
    path("api/", include(reservas.urls)),
    path("api/", include(horario.urls))
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])