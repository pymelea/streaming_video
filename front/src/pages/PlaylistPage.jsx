import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { List, ArrowLeft, Play } from 'lucide-react';
import Header from '../components/layout/Header';
import LoadingSpinner from '../components/common/LoadingSpinner';
import PageError500 from '../components/common/Page500';
import VideoPlayer from '../components/video/VideoPlayer';
import { get } from '../utils/api';
import config from '../config';
import { API_ENDPOINTS } from '../utils/constants';

/**
 * PlaylistPage component displays a playlist and its videos
 * Allows users to browse and play videos from the playlist
 */
const PlaylistPage = () => {
  const { id } = useParams();
  const [playlist, setPlaylist] = useState(null);
  const [videos, setVideos] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentVideoIndex, setCurrentVideoIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);

  // Fetch playlist data and videos
  useEffect(() => {
    const fetchPlaylistData = async () => {
      setIsLoading(true);
      try {
        // Fetch playlist details
        const playlistData = await get(API_ENDPOINTS.PLAYLIST(id));
        setPlaylist(playlistData);

        // Fetch playlist videos
        const videosData = await get(API_ENDPOINTS.PLAYLIST_VIDEOS(id));
        setVideos(videosData);
      } catch (err) {
        console.error('Error fetching playlist data:', err);
        setError(err);
      } finally {
        setIsLoading(false);
      }
    };

    if (id) {
      fetchPlaylistData();
    }
  }, [id]);

  // Handle video selection
  const handleVideoSelect = (index) => {
    setCurrentVideoIndex(index);
    setIsPlaying(true);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  // Handle video end - play next video if available
  const handleVideoEnd = () => {
    if (currentVideoIndex < videos.length - 1) {
      setCurrentVideoIndex(currentVideoIndex + 1);
    } else {
      setIsPlaying(false);
    }
  };

  // Format duration from minutes to human-readable format
  const formatDuration = (minutes) => {
    if (!minutes) return '00:00';
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours}h ${mins}m`;
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-[#0F0F0F] flex justify-center items-center">
        <LoadingSpinner />
      </div>
    );
  }

  if (error || !playlist) {
    return <PageError500 />;
  }

  const currentVideo = videos[currentVideoIndex];

  return (
    <div className="min-h-screen bg-[#0F0F0F]">
      <Header />
      
      <div className="container mx-auto pt-16 px-4">
        {/* Back button */}
        <Link to="/" className="inline-flex items-center text-gray-400 hover:text-white mb-4">
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Home
        </Link>

        {/* Playlist header */}
        <div className="flex items-center mb-6">
          <div className="w-12 h-12 bg-purple-600 rounded-lg flex items-center justify-center mr-4">
            <List className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">{playlist.name}</h1>
            <p className="text-gray-400">{videos.length} videos • {playlist.description}</p>
          </div>
        </div>

        {/* Video player section */}
        {isPlaying && currentVideo && (
          <div className="mb-8">
            <VideoPlayer 
              videoData={currentVideo} 
              isLoading={false} 
              error={null} 
              onEndVideo={handleVideoEnd}
            />
            <h2 className="text-xl font-bold text-white mt-4">{currentVideo.title}</h2>
            <p className="text-gray-400">{formatDuration(currentVideo.duration)} • {currentVideo.year}</p>
          </div>
        )}

        {/* Playlist videos */}
        <div className="bg-[#1A1A1A] rounded-lg overflow-hidden">
          <div className="p-4 border-b border-gray-800 flex justify-between items-center">
            <h3 className="text-white font-medium">Videos in this playlist</h3>
            {!isPlaying && (
              <button 
                className="bg-purple-600 text-white px-4 py-2 rounded-full flex items-center hover:bg-purple-700 transition-colors"
                onClick={() => handleVideoSelect(0)}
              >
                <Play className="w-4 h-4 mr-2" />
                Play All
              </button>
            )}
          </div>
          
          <div className="divide-y divide-gray-800">
            {videos.map((video, index) => (
              <div 
                key={video.id}
                className={`p-4 flex items-center hover:bg-[#252525] cursor-pointer transition-colors ${index === currentVideoIndex && isPlaying ? 'bg-[#252525]' : ''}`}
                onClick={() => handleVideoSelect(index)}
              >
                <div className="w-6 text-center text-gray-500 mr-4">{index + 1}</div>
                <div className="relative w-24 aspect-video bg-[#0F0F0F] mr-4 flex-shrink-0">
                  <img 
                    src={video.thumbnail || 'https://placehold.co/160x90/333/FFF'} 
                    alt={video.title} 
                    className="w-full h-full object-cover"
                  />
                  {index === currentVideoIndex && isPlaying && (
                    <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
                      <div className="w-6 h-6 rounded-full bg-white flex items-center justify-center">
                        <span className="block w-3 h-3 bg-purple-600"></span>
                      </div>
                    </div>
                  )}
                </div>
                <div className="flex-1">
                  <h4 className="text-white font-medium">{video.title}</h4>
                  <p className="text-gray-400 text-sm">{formatDuration(video.duration)} • {video.year}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PlaylistPage;
