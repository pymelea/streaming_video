import React from 'react';
import { Link, useParams } from 'react-router-dom';
import { Video } from 'lucide-react';
import { useGetRecommendedVideos } from '../../hooks/useVideos';
import LoadingSpinner from '../common/LoadingSpinner';

const RecommendedItem = ({ item }) => {
  return (
    <Link to={`/video/${item.id}`} className="flex bg-[#1A1A1A] rounded-lg overflow-hidden hover:bg-[#252525] transition-colors cursor-pointer">
      <div className="relative w-40 aspect-video bg-[#0F0F0F]">
        {item.thumbnail ? (
          <img src={item.thumbnail} alt={item.title} className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <Video className="w-10 h-10 text-gray-600" />
          </div>
        )}
        <div className="absolute bottom-2 right-2 px-1 py-0.5 bg-black/80 text-white text-xs rounded">
          {`${item.watchCount} watching`}
        </div>
      </div>
      <div className="flex-1 p-3">
        <div className="flex items-start justify-between">
          <h3 className="text-white font-medium mb-1 line-clamp-2 flex-1">{item.title}</h3>
          <span className="ml-2 px-1.5 py-0.5 bg-gray-700 rounded text-xs text-white uppercase">video</span>
        </div>
        <p className="text-sm text-gray-400">{item.streamer}</p>
        <p className="text-xs text-purple-400 mt-1">{item.duration}</p>
      </div>
    </Link>
  );
};

const RecommendedStreams = () => {
  // Get current video ID from URL params
  const { id: currentVideoId } = useParams();
  
  // Fetch recommended videos based on current video ID
  const { 
    data: recommendedVideos = [], 
    isLoading: isLoadingVideos,
    error: videosError
  } = useGetRecommendedVideos(currentVideoId);
  
  // Handle loading state
  if (isLoadingVideos) {
    return (
      <div className="flex justify-center items-center h-40">
        <LoadingSpinner />
      </div>
    );
  }
  
  // Handle error state
  if (videosError) {
    return (
      <div className="text-red-500 p-4 bg-red-100 rounded">
        Error loading recommendations. Please try again later.
      </div>
    );
  }
  
  // Format video data for display
  const formattedVideos = recommendedVideos.map(video => ({
    id: video.id,
    title: video.title,
    streamer: video.author || 'Unknown Creator',
    watchCount: video.views ? `${video.views}` : '0',
    duration: video.duration || 'Live',
    thumbnail: video.thumbnail || `https://placehold.co/160x90/333/FFF?text=${encodeURIComponent(video.title)}`
  })).slice(0, 6); // Show up to 6 videos

  return (
    <div>
      <h2 className="text-lg font-bold text-white mb-4">Recommended Videos</h2>
      
      <div className="space-y-4">
        {formattedVideos.length > 0 ? (
          formattedVideos.map((video) => (
            <RecommendedItem
              key={video.id}
              item={video}
            />
          ))
        ) : (
          <p className="text-gray-400 text-sm">No recommended videos available</p>
        )}
      </div>
    </div>
  );
};

export default RecommendedStreams;
