# Anteproyecto DAW

## Título del Proyecto
Información Turística de Ciudades

## Autor del Proyecto
Pablo Enrique Andrada Grimaldi

## Introducción del proyecto (“Qué quiero hacer”)
Mi aplicación web permite a los usuarios buscar información turística sobre cualquier ciudad del mundo. En esta aplicación se mostrará una imagen de la ciudad buscada, información geográfica de la misma, el clima actual y una lista de posibles actividades turísticas. Para ello usaré APIs para obtener la información.

## Finalidad (“Para qué puede servir”)
Esta web puede servir para personas que estén planificando viajes o que quieren conocer información sobre cualquier ciudad del mundo.

## Objetivos (“Una vez puesto en marcha, qué permitirá hacer”)
- Registrar a los usuarios, loguearse y guardar sus ciudades favoritas.
- Permitir la búsqueda de ciudades por parte del usuario.
- Mostrar una imagen de la ciudad usando una API.
- Proporcionar información meteorológica de la ciudad en tiempo real usando una API.
- Listar actividades turísticas a través de una API.
- Mostrar información básica como la población o la ubicación en coordenadas de la ciudad con una API.

## Medios hardware y software a utilizar (“Qué necesito”)
- **Hardware:** Ordenador personal con acceso a internet.
- **Software:**
  - Sistema Operativo: Windows
  - Lenguaje de Programación: Python y JavaScript
  - Framework: Django
  - APIs
  - Base de Datos: PostgreSQL
  - Docker
  - AWS
  - Control de Versiones: GitHub

## Planificación (“Cómo voy a hacerlo, cuánto tiempo creo que tardaré”)
1. **Semana 1:** Investigación de APIs y creación del entorno de desarrollo.
2. **Semana 2:** Desarrollo de la estructura básica del proyecto y formulario de búsqueda.
3. **Semana 3:** Integración de API para mostrar imágenes de la ciudad.
4. **Semana 4:** Integración de la API para mostrar el clima de la ciudad.
5. **Semana 5:** Integración de la API de actividades.
6. **Semana 6:** Diseño del frontend y tests.
7. **Semana 7:** Dockerización, corrección de errores y documentación.
8. **Semana 8:** Despliegue final de la aplicación en AWS.


# TURISTEO
## PASOS PARA INICIAR EL PROGRAMA
1. Con el programa recien instalado nos vamos a la terminal y escribimos
```python

docker compose build

````

2. Despues de que se construya nuestra imagen de docker vamos a levantarlo
```python

docker compose up -d

````

3. Con todo listo podemos acceder al proyecto añadiendo la siguiente ruta dentro del navegador
```python

http://localhost:8000/

````

> [!WARNING]
> **¡ATENCIÓN!**
>
> - Si no funciona el puerto, quizás tengas algún proyecto que utilice el mismo puerto que el de la aplicación. En ese caso, utiliza el siguiente comando para quitar todo lo que tengas activo:
>
>   ```bash
>   docker compose down
>   ```
>
> - Si ves que aún no funciona, puedes probar a borrar todos los contenedores y las imágenes que tengas:
>
>   ```bash
>   docker rm -f $(docker ps -aq)
>   ```
>
>   ```bash
>   docker rmi -f $(docker images -aq)
>   ```
>
> **Recuerda:** si tumbas todos tus servicios, tienes que volver a construir la imagen del proyecto desde cero para que funcione.


## Dockerizado de proyecto

- Para dockerizar el proyecto hemos implementado una serie de archivos para que pueda funcionar de esta manera, hemos utilizado principalmente tres archivos:
  - docker-compose.yml:
    ```python
    version: '3.9'
    
    services:
      db:
        image: postgres:15
        restart: always
        ports:
          - "5432:5432"
        volumes:
          - postgres_data:/var/lib/postgresql/data
        env_file:
          - .env
    
      web:
        build: .
        restart: always
        command: >
          sh -c "python manage.py migrate &&
                 python manage.py runserver 0.0.0.0:8000"
        volumes:
          - .:/app
        ports:
          - "8000:8000"
        env_file:
          - .env
        depends_on:
          - db
    
    volumes:
      postgres_data:
    ```

  - Dockerfile:
    ```python
    # Builder stage
    FROM python:3.12-slim as builder
    WORKDIR /app
    
    RUN apt-get update && apt-get install -y \
        build-essential \
        libpq-dev \
        && rm -rf /var/lib/apt/lists/*
    
    COPY requirements.txt .
    RUN pip install --no-cache-dir --upgrade pip && \
        pip install --no-cache-dir -r requirements.txt
    
    # Final stage
    FROM python:3.12-slim
    WORKDIR /app
    
    COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
    COPY --from=builder /usr/local/bin /usr/local/bin
    
    COPY . .
    
    RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && \
        rm -rf /var/lib/apt/lists/* && \
        useradd -m myuser && \
        chown -R myuser:myuser /app && \
        mkdir -p /app/staticfiles /app/media && \
        chown -R myuser:myuser /app/staticfiles /app/media
    
    USER myuser
    
    ENV DEBUG=True \
        PORT=8000 \
        PYTHONUNBUFFERED=1 \
        PYTHONPATH=/app
    
    RUN python manage.py collectstatic --noinput
    
    EXPOSE 8000
    CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
    ```

  - requirements.txt:
    ```python
    ﻿asgiref==3.8.1
    certifi==2025.4.26
    charset-normalizer==3.4.2
    crispy-bootstrap5==2025.4
    Django==5.2.1
    django-cleanup==9.0.0
    django-countries==7.6.1
    django-crispy-forms==2.4
    idna==3.10
    pillow==11.2.1
    python-dotenv==1.1.0
    requests==2.32.3
    sqlparse==0.5.3
    typing_extensions==4.13.2
    tzdata==2025.2
    urllib3==2.4.0
    pytest==8.2.1
    gunicorn==20.1.0
    psycopg2-binary==2.9.10
    ```
