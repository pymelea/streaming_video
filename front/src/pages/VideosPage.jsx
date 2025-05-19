import React from 'react';
import { Link } from 'react-router-dom';
import { Video } from 'lucide-react';
import Header from '../components/layout/Header';
import LoadingSpinner from '../components/common/LoadingSpinner';
import PageError500 from '../components/common/Page500';
import { useGetVideos } from '../hooks/useVideos';

/**
 * VideosPage component displays all available videos
 */
const VideosPage = () => {
  // Use the hook to fetch videos
  const { data: videos = [], isLoading, error } = useGetVideos();

  // Format duration from minutes to human-readable format
  const formatDuration = (minutes) => {
    if (!minutes) return '00:00';
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours}h ${mins}m`;
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-[#0F0F0F]">
        <Header />
        <div className="container mx-auto pt-24 px-4 flex justify-center">
          <LoadingSpinner />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-[#0F0F0F]">
        <Header />
        <div className="container mx-auto pt-24 px-4">
          <PageError500 />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0F0F0F]">
      <Header />
      <div className="container mx-auto pt-24 px-4 pb-12">
        <h1 className="text-3xl font-bold text-white mb-8">All Videos</h1>
        
        {videos.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-400 text-lg">No videos available.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {videos.map((video) => (
              <Link
                key={video.id}
                to={`/video/${video.id}`}
                className="bg-[#1A1A1A] rounded-lg overflow-hidden hover:bg-[#252525] transition-all duration-300 group"
              >
                <div className="relative aspect-video bg-[#0F0F0F]">
                  <img
                    src={video.thumbnail ?? 'https://placehold.co/320x180'}
                    alt={video.title}
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity">
                    <div className="absolute bottom-4 left-4">
                      <span className="px-2 py-1 bg-red-600 text-white text-sm rounded">
                        {video.categories?.join(', ') || "HOME"}
                      </span>
                    </div>
                  </div>
                  <div className="absolute top-3 right-3 bg-black/70 px-2 py-1 rounded text-white text-xs flex items-center">
                    <Video className="w-3 h-3 mr-1" />
                    {formatDuration(video.duration)}
                  </div>
                </div>
                <div className="p-4">
                  <h3 className="text-white font-medium text-lg mb-2 truncate">{video.title}</h3>
                  <div className="flex items-center justify-between">
                    <p className="text-sm text-gray-400 font-medium">{video.year ?? "Unknown Year"}</p>
                    <span className="text-xs text-purple-400">{video.views ? `${video.views} views` : "0 views"}</span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default VideosPage;
