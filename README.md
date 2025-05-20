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

## 🏗️ Project Structure

```plaintext
stream_apifast_v1/
├── back/                 # Backend (FastAPI)
│   ├── api/              # API endpoints definition
│   ├── core/             # Core configurations
│   ├── db/               # Database configuration
│   ├── models/           # Data models
│   ├── schemas/          # Validation schemas
│   ├── services/         # Business logic
│   ├── tests/            # Unit and integration tests
│   └── main.py           # Application entry point
├── front/                # Frontend (React + Vite)
│   ├── public/           # Static files
│   ├── src/              # React source code
│   └── package.json      # Dependencies and scripts
└── infra/                # Infrastructure configuration
```

## 🚦 How to install and run the project

### What you need before starting

To install and run this platform on your computer, you will need to have the following installed:

- **Python 3.10 or higher**: This is the programming language used by the server side. [How to install Python](https://www.python.org/downloads/)

- **Node.js 18 or higher**: This is necessary to run the visual part of the application. [How to install Node.js](https://nodejs.org/)

- **Database**: By default, the application can use SQLite (which requires no additional installation), but for more advanced use, you can use PostgreSQL. [How to install PostgreSQL](https://www.postgresql.org/download/)

### Step 1: Configure the server side (Backend)

Follow these steps in order. If you encounter any errors, the message will generally give you clues on how to fix them.

```bash
# Navigate to the backend directory
cd back

# Install dependencies and create virtual environment with Poetry
poetry install

# Activate the Poetry virtual environment
poetry env activate

# Prepare the database
make up_db



# Start the server
poetry run python main.py
```

The API server will be available at [http://localhost:8000/docs](http://localhost:8000/docs)

Now you need to open **another terminal** (leave the previous one open) and follow these steps:

```bash
# Navigate to the frontend directory
cd front

# Install dependencies
npm install

# Start the development server
npm run dev
```

The application will be available at [http://localhost:3000](http://localhost:3000)

## 📚 API Documentation

The interactive API documentation is available at:


- Doc: [http://localhost:8000/docs](http://localhost:8000/docs)

## 🧪 Tests

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

## 🤝 Want to help improve this platform?

Your contributions are very welcome. If you have programming knowledge and want to help, these are the basic steps:

1. Fork the repository
2. Create a branch for your feature (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

If you have questions or suggestions, don't hesitate to contact me.

---

Developed with ❤️ by Lily Perera from Streaming Video Platform
