from dotenv import load_dotenv
from pathlib import Path
import os

from celery.schedules import crontab



BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()
SECRET_KEY = 'django-insecure-%n!)s(pm^e-udpj9&2ti*1_!)8gtap2dp8&!th36@nefc6ukub'
DEBUG = True

#Información que se supone que debe de ser confidencial 
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
PEIGO_QR_URL = "https://upload.wikimedia.org/wikipedia/commons/5/5e/QR_Code_example.png"
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

ALLOWED_HOSTS = []
CELERY_BEAT_SCHEDULE = {
    'rechazar_reservas_vencidas_diario': {
        'task': 'reservas.tasks.rechazar_reservas_vencidas_diario',
        'schedule': crontab(hour=23,minute=0),  # Corre todos los días a medianoche
    },
     'recordatorio-admin-cada-2-horas': {
        'task': 'reservas.tasks.recordatorio_reservas_pendientes',
        'schedule': crontab(minute=0, hour='*/2'),  # Cada 2 horas
    },
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
     #Nuestras apps 
     'reservas.apps.ReservasConfig',
     'horario',
     'cancha',
     'profiles',
     #Librerias instaladas
     'rest_framework',
     'corsheaders'
]

MIDDLEWARE = [
     'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'FutZone.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'FutZone.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'profiles.authentication.SupabaseRemoteAuth',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE':10
    
}
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173", 
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'bdd_titulacion',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}




AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')  # Carpeta donde tú pones tus archivos estáticos
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Solo se usa en producción

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
