# 🎬 Plataforma de Streaming de Video

¡Bienvenido/a a nuestra Plataforma de Streaming de Video! Este proyecto te permite crear tu propio servicio de streaming similar a Netflix o YouTube, donde podrás subir, organizar y reproducir videos con una interfaz moderna y atractiva.

## 📸 Capturas de Pantalla

### Interfaz Principal

![Interfaz Principal](/screenshots/main_interface.png)
*Vista principal de la aplicación mostrando la lista de videos disponibles*

### Reproductor de Video

![Reproductor de Video](/screenshots/video_player.png)
*Reproductor de video con controles y subtítulos*


### Documentación API (Stream API)

![OpenAPI](/screenshots/swagger_ui.png)
*Documentación interactiva de la API*

## 📋 ¿Qué es esta plataforma?

Esta aplicación es una plataforma completa para ver videos en línea (streaming), similar a servicios como Netflix, YouTube o Disney+, pero que puedes instalar y personalizar según tus necesidades. Está diseñada para ser fácil de usar tanto para los espectadores como para los administradores.

### ¿Para qué sirve?

- **Para usuarios**: Permite ver videos organizados por categorías, crear listas de reproducción personalizadas y disfrutar de contenido con subtítulos en diferentes idiomas.

- **Para administradores**: Facilita la subida de videos, organización del contenido y gestión de usuarios de manera sencilla.

### ¿Cómo está construida?

La plataforma consta de dos partes principales:

1. **Backend (parte trasera)**: Es el "cerebro" de la aplicación que maneja todos los datos y la lógica. Está construido con FastAPI, un moderno framework de Python que hace que todo funcione rápido y de manera eficiente.

2. **Frontend (parte delantera)**: Es lo que los usuarios ven e interactúan. Está desarrollado con React, una tecnología que permite crear interfaces atractivas y fáciles de usar.

## 🚀 ¿Qué puedes hacer con esta plataforma?

Esta plataforma ofrece muchas funciones que la hacen completa y fácil de usar:

### Para los espectadores

- **Explorar videos por categorías**: Encuentra fácilmente el contenido que te interesa, ya sea películas, series, documentales o cualquier otra categoría que decidas crear.

- **Crear tus propias listas de reproducción**: Guarda tus videos favoritos en listas personalizadas para verlos más tarde, similar a como lo harías en YouTube o Spotify.

- **Ver videos con subtítulos**: Disfruta del contenido con subtítulos en diferentes idiomas, ideal para aprender idiomas o para personas con discapacidad auditiva.

- **Reproductor de video avanzado**: Controles intuitivos para pausar, adelantar, retroceder, ajustar el volumen y cambiar la calidad del video.

### Para los administradores

- **Panel de control sencillo**: Administra todo el contenido desde una interfaz fácil de usar, sin necesidad de conocimientos técnicos avanzados.

- **Subida de videos simplificada**: Sube nuevos videos al sistema con unos pocos clics, añadiendo automáticamente información como título, descripción y portada.

- **Organización automática**: El sistema puede clasificar automáticamente los videos según su género o tipo de contenido.

- **Estadísticas de visualización**: Conoce qué videos son más populares y cuáles son los patrones de visualización de tus usuarios.

### Características técnicas (para desarrolladores)

- **API completa y documentada**: Si eres desarrollador, puedes integrar esta plataforma con otros sistemas gracias a su API bien documentada.

- **Diseño adaptable**: La interfaz se ajusta automáticamente a cualquier dispositivo, ya sea computadora, tablet o teléfono móvil.

## 🛠️ Tecnologías utilizadas (explicado de forma sencilla)

Esta sección explica las herramientas que usamos para construir la plataforma. No te preocupes si no entiendes todos estos términos, no necesitas conocerlos para usar la aplicación.

### Parte del servidor (Backend)

- **FastAPI**: Es como el "cerebro" de la aplicación. Procesa todas las peticiones y gestiona los datos de manera rápida y eficiente.

- **Base de datos (SQLAlchemy)**: Es como una biblioteca digital muy organizada donde guardamos toda la información: videos, usuarios, categorías, etc.

- **Validación de datos (Pydantic)**: Es como un guardia de seguridad que verifica que toda la información que entra y sale de la aplicación sea correcta.

- **Servidor web (Uvicorn)**: Es como un camarero que sirve la aplicación a través de internet para que todos puedan acceder a ella.

### Parte visual (Frontend)

- **React**: Es como el arquitecto y diseñador de interiores que crea todas las pantallas que ves e interactúas.

- **Navegación (React Router)**: Es como el sistema de señalización que te permite moverte entre diferentes secciones de la aplicación.

- **Gestión de datos (React Query)**: Es como un asistente eficiente que se encarga de traer y actualizar la información que ves en pantalla.

- **Reproductor de video (React Player)**: Es la televisión inteligente que reproduce los videos con todos los controles necesarios.

- **Diseño adaptable (TailwindCSS)**: Es como un diseñador de moda que hace que la aplicación se vea bien en cualquier dispositivo, ya sea un teléfono, tablet o computadora.

- **Construcción rápida (Vite)**: Es como un constructor super veloz que ensambla todas las piezas de la aplicación para que funcione rápidamente.

## 🏗️ Estructura del Proyecto

```plaintext
stream_apifast_v1/
├── back/                 # Backend (FastAPI)
│   ├── api/              # Definición de endpoints API
│   ├── core/             # Configuraciones centrales
│   ├── db/               # Configuración de base de datos
│   ├── models/           # Modelos de datos
│   ├── schemas/          # Esquemas de validación
│   ├── services/         # Lógica de negocio
│   ├── tests/            # Tests unitarios y de integración
│   └── main.py           # Punto de entrada de la aplicación
├── front/                # Frontend (React + Vite)
│   ├── public/           # Archivos estáticos
│   ├── src/              # Código fuente React
│   └── package.json      # Dependencias y scripts
└── infra/                # Configuración de infraestructura
```

## 🚦 Cómo instalar y ejecutar el proyecto

### Lo que necesitas antes de empezar

Para poder instalar y ejecutar esta plataforma en tu computadora, necesitarás tener instalado lo siguiente:

- **Python 3.10 o superior**: Es el lenguaje de programación que usa la parte del servidor. [Cómo instalar Python](https://www.python.org/downloads/)

- **Node.js 18 o superior**: Es necesario para ejecutar la parte visual de la aplicación. [Cómo instalar Node.js](https://nodejs.org/)

- **Base de datos**: Por defecto, la aplicación puede usar SQLite (que no requiere instalación adicional), pero para un uso más avanzado puedes usar PostgreSQL. [Cómo instalar PostgreSQL](https://www.postgresql.org/download/)

### Paso 1: Configurar la parte del servidor (Backend)

Sigue estos pasos en orden. Si encuentras algún error, generalmente el mensaje te dará pistas sobre cómo solucionarlo.

```bash
# Navegar al directorio del backend
cd back

# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# 6. Prepara la base de datos
python run_migrations.py

# 7. (Opcional) Carga datos de ejemplo para probar
python -m seeds.seed_all

# 8. Inicia el servidor
python main.py
```

El servidor API estará disponible en [http://localhost:8000](http://localhost:8000)

Ahora necesitas abrir **otra terminal** (deja la anterior abierta) y seguir estos pasos:

```bash
# Navegar al directorio del frontend
cd front

# Instalar dependencias
npm install

# Iniciar el servidor de desarrollo
npm run dev
```

La aplicación estará disponible en [http://localhost:3000](http://localhost:3000)

## 📚 Documentación API

La documentación interactiva de la API está disponible en:


- Doc: [http://localhost:8000/docs](http://localhost:8000/docs)

## 🧪 Pruebas

### Backend

```bash
cd back
pytest
```

### Frontend

```bash
cd front
npm test
```

## 🤝 ¿Quieres ayudar a mejorar esta plataforma?

Tus contribuciones son muy bienvenidas. Si tienes conocimientos de programación y quieres ayudar, estos son los pasos básicos:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/amazing-feature`)
3. Haz commit de tus cambios (`git commit -m 'Add some amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 📞 Contacto

Si tienes preguntas o sugerencias, no dudes en contactarme.

---

Desarrollado con ❤️ por el Lily Perera de Streaming Video Platform
