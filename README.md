# 🎬 Video Streaming Platform

Welcome to our Video Streaming Platform! This project allows you to create your own streaming service similar to Netflix or YouTube, where you can upload, organize, and play videos with a modern and attractive interface.

## 📸 Screenshots

### Main Interface

![Main Interface](/screenshots/main_interface.png)
*Main view of the application showing the list of available videos*

### Video Player

![Video Player](/screenshots/video_player.png)
*Video player with controls and subtitles*


### API Documentation (Stream API)

![OpenAPI](/screenshots/swagger_ui.png)
*Interactive API documentation*

## 📋 What is this platform?

This application is a complete platform for watching videos online (streaming), similar to services like Netflix, YouTube, or Disney+, but you can install and customize it according to your needs. It is designed to be easy to use for both viewers and administrators.

### What is it for?

- **For users**: It allows viewing videos organized by categories, creating custom playlists, and enjoying content with subtitles in different languages.

- **For administrators**: It facilitates uploading videos, organizing content, and managing users in a simple way.

### How is it built?

The platform consists of two main parts:

1. **Backend**: It's the "brain" of the application that handles all the data and logic. It's built with FastAPI, a modern Python framework that makes everything work quickly and efficiently.

2. **Frontend**: It's what users see and interact with. It's developed with React, a technology that allows creating attractive and easy-to-use interfaces.

## 🚀 What can you do with this platform?

This platform offers many features that make it complete and easy to use:

### For viewers

- **Browse videos by categories**: Easily find content that interests you, whether it's movies, series, documentaries, or any other category you decide to create.

- **Create your own playlists**: Save your favorite videos in custom lists to watch later, similar to how you would on YouTube or Spotify.

- **Watch videos with subtitles**: Enjoy content with subtitles in different languages, ideal for learning languages or for people with hearing impairments.

- **Advanced video player**: Intuitive controls to pause, fast forward, rewind, adjust volume, and change video quality.

### For administrators

- **Simple control panel**: Manage all content from an easy-to-use interface, without the need for advanced technical knowledge.

- **Simplified video upload**: Upload new videos to the system with just a few clicks, automatically adding information such as title, description, and cover.

- **Automatic organization**: The system can automatically classify videos according to their genre or content type.

- **Viewing statistics**: Know which videos are most popular and what the viewing patterns of your users are.

### Technical features (for developers)

- **Complete and documented API**: If you are a developer, you can integrate this platform with other systems thanks to its well-documented API.

- **Responsive design**: The interface automatically adjusts to any device, whether it's a computer, tablet, or mobile phone.

## 🛠️ Technologies used (explained in simple terms)

This section explains the tools we use to build the platform. Don't worry if you don't understand all these terms; you don't need to know them to use the application.

### Server side (Backend)

- **FastAPI**: It's like the "brain" of the application. It processes all requests and manages data quickly and efficiently.

- **Database (SQLAlchemy)**: It's like a highly organized digital library where we store all the information: videos, users, categories, etc.

- **Data validation (Pydantic)**: It's like a security guard that verifies that all information entering and leaving the application is correct.

- **Web server (Uvicorn)**: It's like a waiter that serves the application over the internet so everyone can access it.

### Visual side (Frontend)

- **React**: It's like the architect and interior designer that creates all the screens you see and interact with.

- **Navigation (React Router)**: It's like the signaling system that allows you to move between different sections of the application.

- **Data management (React Query)**: It's like an efficient assistant who is responsible for bringing and updating the information you see on screen.

- **Video player (React Player)**: It's the smart TV that plays videos with all the necessary controls.

- **Responsive design (TailwindCSS)**: It's like a fashion designer that makes the application look good on any device, whether it's a phone, tablet, or computer.

- **Fast building (Vite)**: It's like a super-fast builder that assembles all the pieces of the application to make it work quickly.

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
