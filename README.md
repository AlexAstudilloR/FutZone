# API REST de Gestión de Canchas y Reservas

Esta API REST está construida con Django y Django REST Framework. Permite gestionar canchas deportivas, horarios, perfiles de usuario y reservas.

## Requisitos

- Python 3.8+
- Django 3.x o superior
- Django REST Framework
- Supabase Auth configurado para autenticación de usuarios

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd nombre_proyecto
   ```

2. Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate   # Windows
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configurar variables de entorno en `.env`:
   - `DATABASE_URL`
   - `SECRET_KEY`
   - `SUPABASE_URL`
   - `SUPABASE_KEY`

5. Ejecutar migraciones:
   ```bash
   python manage.py migrate
   ```

6. Iniciar servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

La API estará disponible en `http://localhost:8000/api/`.

---

## Autenticación

Se utiliza **Supabase Auth** para la gestión de usuarios mediante correo electrónico y contraseña.

- **Registro y login:** 
  - Ruta unificada en Supabase (externo a la API Django).
  - Campos requeridos: 
    - `email`
    - `password`
  - Al registrarse, Supabase crea el usuario y emite tokens JWT que deben incluirse en:
    ```
    Authorization: Bearer <access_token>
    ```

- **ProfileModel**  
  Además de `email` y `password`, al crear el usuario se genera simultáneamente un registro en `ProfileModel` con los campos:
  - `id`: UUID automático
  - `full_name`: texto (opcional)
  - `cell_phone`: texto (opcional)
  - `status`: booleano
  - `is_admin`: booleano
  - `created_at`: datetime de creación
  - `updated_at`: datetime de última actualización

- **Obtener mi perfil:**
  - `GET /api/auth/mi-perfil/`
  - Requiere header de autorización.

---

## Endpoints

### Canchas

- **Listar canchas**  
  `GET /api/canchas/`

- **Crear cancha**  
  `POST /api/canchas/`  
  Body:  
  ```json
  { "name": "Cancha 1", "location": "Ciudad" }
  ```

- **Detalle de cancha**  
  `GET /api/canchas/{id}/`

- **Actualizar cancha**  
  `PUT /api/canchas/{id}/`

- **Eliminar cancha**  
  `DELETE /api/canchas/{id}/`

### Horarios Semanales

- **Listar horarios**  
  `GET /api/weekly-schedules/`

- **Crear horario**  
  `POST /api/weekly-schedules/`  
  Body ejemplo:
  ```json
  {
    "field": 1,
    "day_of_week": "Monday",
    "start_time": "08:00",
    "end_time": "10:00"
  }
  ```

- **Detalle / Actualizar / Eliminar**  
  `GET|PUT|DELETE /api/weekly-schedules/{pk}/`

### Excepciones de Fecha

- **Listar excepciones**  
  `GET /api/date-exceptions/`

- **Crear excepción**  
  `POST /api/date-exceptions/`  
  Body ejemplo:
  ```json
  {
    "field": 1,
    "date": "2025-07-15",
    "start_time": "14:00",
    "end_time": "16:00"
  }
  ```

- **Detalle / Actualizar / Eliminar**  
  `GET|PUT|DELETE /api/date-exceptions/{pk}/`

- **Obtener excepciones por fecha**  
  `GET /api/date-exceptions/exceptions/?date=YYYY-MM-DD`

### Perfiles de Usuario

- **Listar perfiles**  
  `GET /api/auth/profiles/`

- **Crear perfil**  
  `POST /api/auth/profiles/`  
  Body ejemplo:
  ```json
  {
    "full_name": "Juan Pérez",
    "cell_phone": "+593987654321",
    "status": true,
    "is_admin": false
  }
  ```

- **Detalle / Actualizar / Eliminar**  
  `GET|PUT|DELETE /api/auth/profiles/{pk}/`

- **Mi perfil**  
  `GET /api/auth/mi-perfil/`

### Reservas

- **Listar y crear reservas**  
  `GET /api/reservas/`  
  `POST /api/reservas/`

- **Detalle / Actualizar / Eliminar**  
  `GET|PUT|DELETE /api/reservas/{pk}/`

- **Reservas por fecha**  
  `GET /api/reservas/fecha/?date=YYYY-MM-DD`

- **Resumen diario de reservas**  
  `GET /api/summary/?date=YYYY-MM-DD`

---

## Ejemplos de uso con `curl`

```bash
# Obtener mi perfil
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/auth/mi-perfil/

# Crear un perfil (supabase crea primero, luego en Django)
curl -X POST -H "Authorization: Bearer <token>" -H "Content-Type: application/json" \
  -d '{"full_name":"Juan Pérez","cell_phone":"+593987654321","status":true,"is_admin":false}' \
  http://localhost:8000/api/auth/profiles/
```

---
