# myproject/celery.py

import os
from celery import Celery

# Establece el módulo de configuración de Django por defecto para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FutZone.settings')

# Crea la instancia de Celery con el nombre de tu proyecto
app = Celery('FutZone')

# Carga la configuración desde settings.py usando el prefijo CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodescubre tareas en todos los apps registrados (tasks.py)
app.autodiscover_tasks()

# (opcional) muestra qué tarea se está ejecutando
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
