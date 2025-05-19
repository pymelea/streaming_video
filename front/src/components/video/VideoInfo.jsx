import React from 'react';
import PageError500 from '../common/Page500';
import LoadingSpinner from '../common/LoadingSpinner';

/**
 * A component that displays information about a video.
 * 
 * @param {{ data: Video, isLoading: boolean, error: Error }} props
 * @prop {Video} data - The video data to display.
 * @prop {boolean} isLoading - Whether the video data is still loading.
 * @prop {Error} error - An error that occurred while loading the video data.
 */
const VideoInfo = ({ data ,isLoading,error }) => {

  if (error) {
    return <PageError500 />;
  }

  if (isLoading) {
    return <LoadingSpinner />;
  }

  return (
    <div className="bg-[#1A1A1A] rounded-lg p-4">
      <h1 className="text-xl font-bold text-white mb-2">{data.title || 'Unknown Title'}</h1>
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center">
          <div>
            <h3 className="text-white font-medium">{data.categories ? data.categories.join(', ') : 'No categories'}</h3>
            <p className="text-sm text-gray-400">Year {data.year || 'Unknown'}</p>
          </div>
        
        </div>
      </div>
      <div className="bg-[#252525] rounded-lg p-4">
        
        <p className="text-gray-300">
          {data.description || 'No description available'}
        </p>
      </div>
    </div>
  );
};

export default VideoInfo;
