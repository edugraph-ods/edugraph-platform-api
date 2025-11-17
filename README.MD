# EduGraph Platform API

## 📚 Descripción

EduGraph Platform API es el núcleo del ecosistema EduGraph, diseñado para ofrecer servicios backend robustos que permiten la planificación y optimización de rutas de aprendizaje para estudiantes universitarios. Esta API RESTful, construida con FastAPI, se integra con el frontend y los módulos de algoritmos para ofrecer una experiencia educativa personalizada.

## 🚀 Características Principales

- Gestión de usuarios y autenticación
- Administración de planes de estudio y mallas curriculares
- Integración con el módulo de algoritmos para generación de rutas
- API RESTful documentada con OpenAPI
- Soporte para múltiples universidades y planes de estudio
- Sistema de recomendación de cursos basado en rendimiento académico

## 🛠️ Requisitos Previos

- Python 3.8+
- pip (gestor de paquetes de Python)
- PostgreSQL (base de datos)
- Redis (para caché y colas de tareas)

## 🚀 Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/edugraph-ods/edugraph-platform-api.git
   cd edugraph-platform-api
   ```

2. Crea un entorno virtual y actívalo:
   ```bash
    py -m venv .venv
    .\.venv\Scripts\Activate
   ```

3. Configura las variables de entorno:
   ```bash
   cp .env.example .env
   ```

## 🔧 Dependencias Principales

### Core
- **FastAPI**: Framework web moderno y rápido para construir APIs con Python 3.7+
  ```bash
  pip install "fastapi[standard]"
  ```
- **Pydantic**: Validación de datos y configuración mediante anotaciones de tipos
  ```bash
  pip install "pydantic[email]"
  ```
- **Starlette**: Framework ASGI ligero (incluido con FastAPI)
  ```bash
  pip install starlette
  ```
- **SQLAlchemy**: ORM y herramientas de base de datos
  ```bash
  pip install sqlalchemy
  ```
- **Alembic**: Migraciones de base de datos
  ```bash
  pip install alembic
  ```

### Base de Datos
- **asyncpg**: Controlador asíncrono de PostgreSQL
  ```bash
  pip install asyncpg
  ```
- **psycopg2-binary**: Adaptador PostgreSQL para Python
  ```bash
  pip install psycopg2-binary
  ```

### Autenticación y Seguridad
- **python-jose**: Implementación de JWT en Python
  ```bash
  pip install python-jose[cryptography]
  ```
- **passlib**: Biblioteca de hash de contraseñas
  ```bash
  pip install passlib[bcrypt]
  ```

### Desarrollo
- **uvicorn**: Servidor ASGI para ejecutar la aplicación
  ```bash
  pip install uvicorn
  ```
- **pytest**: Framework de pruebas
  ```bash
  pip install pytest
  ```
- **black**: Formateador de código
  ```bash
  pip install black
  ```
- **isort**: Ordenador de importaciones
  ```bash
  pip install isort
  ```

## 🚀 Iniciar la Aplicación

1. Asegúrate de tener PostgreSQL y Redis en ejecución
2. Configura las variables de entorno en `.env`
3. Instala las dependencias:
   ```bash
   python -m pip install fastapi uvicorn sqlalchemy asyncmy passlib[bcrypt] python-jose[cryptography] pydantic-settings email-validator
   ```
4. Inicia el servidor de desarrollo:
   ```bash
   python -m uvicorn app.main:app --reload
   ```
5. Accede a la documentación interactiva en:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

