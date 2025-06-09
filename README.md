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

<font color="red">¡Atención!</font>

- Si no funciona el puerto quizas tengas algun proyecto que utilice el mismo puerto que el de la aplicacion, en ese caso utiliza el siguiente comando para quitar todo lo que tengas activo
```python

docker compose down

```

- Si ves que aun no funciona puedes probar a borrar todos los contenedores y las imagenes que tengas
```python

docker rm -f $(docker ps -aq)

```
```python

docker rmi -f $(docker images -aq)

```

Recuerda: si tumbas todos tus servicios tienes que volver a construir la imagen del proyecto desde cero para que funcione
