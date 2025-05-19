
import { Routes, Route } from "react-router-dom";

import HomePage from "./pages/HomePage";
import ErrorPage from "./pages/ErrorPage";
import PageError404 from "./components/common/Page404";
import VideoPage from "./pages/VideoPage";
import VideosPage from "./pages/VideosPage";
import PlaylistPage from "./pages/PlaylistPage";
import PlaylistsPage from "./pages/PlaylistsPage";

function App() {
  return (
    <div className="bg-gray-100 min-h-screen">
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/error" element={<ErrorPage />} />
        <Route path="/videos" element={<VideosPage />} />
        <Route path="/video/:id" element={<VideoPage />} />
        <Route path="/playlist" element={<PlaylistsPage />} />
        <Route path="/playlist/:id" element={<PlaylistPage />} />
        <Route path="*" element={<PageError404 />} />
      </Routes>
    </div>
  );
}

export default App;
