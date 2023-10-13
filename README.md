# devops_project

## Requisitos

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Python 3.x (para desarrollo local)

# Ejecuta el siguiente comando para construir y ejecutar los contenedores de Docker

```bash
docker-compose -f local.yml build
```

```bash
docker-compose -f local.yml up
```

# Estructura del Proyecto

- `.envs/`: Archivos para variables de entorno.
- `.resources/`: Recursos de apoyo para el proyecto.
- `blacklist/`: Código fuente de la aplicación Flask.
- `local.yml`: Configuración de Docker Compose.
- `README.md`: Documentación del proyecto.
- `requirements.txt`: Listado de dependencias de Python.
- `.resources/API.postman_collection.json`: Collection de Postman para probar la API.