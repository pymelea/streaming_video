import React from 'react';
import ReactPlayer from 'react-player';
import config from '../../config';
import PropTypes from 'prop-types';

  /**
   * Component to display a video player with live streaming support.
   *
   * If the video is not loading, it shows a loading message.
   * If there is an error with the video, it shows an error message.
   * If the video finishes playing, it calls the onEndVideo callback.
   *
   * It also displays a badge indicating that the video is live.
   *
   * @param {boolean} isLoading - Whether the video is still loading.
   * @param {object} error - The error object if there is an issue with the video.
   * @param {object} videoData - The video data object containing the stream URL and thumbnail.
   * @param {function} onEndVideo - The callback called when the video finishes playing.
   */
const VideoPlayer = ({ isLoading, error, videoData, onEndVideo }) => {


  const urlStream = `${config.api.baseUrl}${videoData?.stream_url}`;



  const handleEndVideo = () => {
    if (onEndVideo) {
      onEndVideo();
    }
  };

  const handleDuration = (duration) => {
    console.log('Duration:', duration);
  };


  if (isLoading) {
    return (
      <div className="aspect-video bg-[#0F0F0F] flex items-center justify-center">
        <span className="px-3 py-1 bg-gray-700 text-white rounded">Loading...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="aspect-video bg-[#0F0F0F] flex items-center justify-center">
        <span className="px-3 py-1 bg-red-600 text-white rounded">Error loading video</span>
      </div>
    );
  }

  return (
    <div className="relative">
      <div className="video-container" style={{ aspectRatio: '16/9', width: '100%', backgroundColor: '#000' }}>
        <ReactPlayer
          url={urlStream}
          width="100%"
          height="100%"
          playing={true}
          controls={true}
          onEnded={handleEndVideo}
          onDuration={handleDuration}
          light={videoData?.thumbnail || 'https://placehold.co/640x360'}
          config={{
            file: {
              attributes: {
                crossOrigin: "anonymous",
                controlsList: "nodownload",
                // Ensure native subtitles are displayed
                playsInline: true
              },
              // HLS configuration for better streaming compatibility
              forceHLS: false,
              forceDASH: false,
              // Subtitles configuration
              tracks: videoData?.subtitles_urls && videoData.subtitles_urls.length > 0 
                ? videoData.subtitles_urls.map((subtitle, index) => {
                    const subtitleUrl = `${config.api.baseUrl}${subtitle}`;
                    return {
                      kind: 'subtitles',
                      src: subtitleUrl,
                      srcLang: 'en',
                      label: 'English',
                      default: index === 0 // Only set the first subtitle as default
                    };
                  })
                : []
            }
          }}
        />
      </div>
      <div className="absolute top-4 right-4 z-10">
        <span className="px-3 py-1 bg-red-600 text-white rounded">LIVE</span>
      </div>
    </div>
  );
};

export default VideoPlayer;


VideoPlayer.propTypes = {
  isLoading: PropTypes.bool.isRequired,
  error: PropTypes.object.isRequired,
  videoData: PropTypes.object.isRequired,
  onEndVideo: PropTypes.func.isRequired
};
