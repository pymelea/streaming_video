# Stream API - Backend

## Arquitectura en Capas

Este proyecto implementa una arquitectura en capas para mejorar la organización, mantenibilidad y testabilidad del código. La estructura del proyecto se divide en las siguientes capas:

### 1. Capa de Presentación (API)

Maneja las solicitudes HTTP y las respuestas. Esta capa está implementada en los siguientes directorios:

- `api/`: Contiene los endpoints de la API y la configuración de las rutas.
  - `api/endpoints/`: Endpoints específicos para cada recurso (videos, subtítulos, etc.).
  - `api/dependencies.py`: Dependencias comunes para los endpoints.

### 2. Capa de Servicios

Contiene la lógica de negocio de la aplicación. Esta capa está implementada en el directorio:

- `services/`: Servicios que implementan la lógica de negocio para cada recurso.

### 3. Capa de Acceso a Datos (Repositorios)

Maneja las operaciones de base de datos. Esta capa está implementada en los siguientes directorios:

- `db/repositories/`: Repositorios para cada entidad que abstraen las operaciones de base de datos.
- `db/database.py`: Configuración de la base de datos y sesiones.

### 4. Capa de Modelos

Define las entidades de la base de datos. Esta capa está implementada en el directorio:

- `models/`: Modelos SQLAlchemy para cada entidad.

### 5. Capa de Esquemas

Define los esquemas de datos para la validación y serialización. Esta capa está implementada en el directorio:

- `schemas/`: Esquemas Pydantic para cada entidad.

### 6. Capa de Configuración

Contiene la configuración centralizada de la aplicación. Esta capa está implementada en el directorio:

- `core/`: Configuración centralizada y utilidades comunes.

### 7. Capa de Utilidades

Contiene funciones y clases de utilidad. Esta capa está implementada en el directorio:

- `utils/`: Funciones y clases de utilidad.

## Flujo de Datos

El flujo de datos en la aplicación sigue el siguiente patrón:

1. Las solicitudes HTTP llegan a los endpoints en la capa de presentación (API).
2. Los endpoints llaman a los servicios en la capa de servicios.
3. Los servicios implementan la lógica de negocio y llaman a los repositorios en la capa de acceso a datos.
4. Los repositorios realizan operaciones en la base de datos utilizando los modelos.
5. Los datos se serializan/deserializan utilizando los esquemas Pydantic.
6. Las respuestas se devuelven a través de la capa de presentación.

## Ventajas de la Arquitectura en Capas

- **Separación de Responsabilidades**: Cada capa tiene una responsabilidad específica.
- **Mantenibilidad**: Es más fácil mantener y evolucionar el código.
- **Testabilidad**: Es más fácil escribir pruebas unitarias para cada capa.
- **Reutilización**: Los componentes pueden reutilizarse en diferentes partes de la aplicación.
- **Escalabilidad**: Es más fácil escalar la aplicación horizontalmente.

## Ejecución del Proyecto

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python main.py
```

## Pruebas

```bash
# Ejecutar todas las pruebas
make test

# Ejecutar pruebas con cobertura
make test-cov
```
