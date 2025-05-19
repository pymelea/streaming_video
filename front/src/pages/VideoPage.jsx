import React from 'react';
import { useParams } from 'react-router-dom';
import { useGetVideo } from '../hooks/useVideos';
import VideoPlayer from '../components/video/VideoPlayer';
import VideoInfo from '../components/video/VideoInfo';
import RecommendedStreams from '../components/video/RecommendedStreams';
import Header from '../components/layout/Header';

const VideoPage = () => {
    const { id } = useParams();
    const { data, isLoading, error } = useGetVideo(id);

    return (
        <div className="pt-14 pb-20 min-h-screen bg-[#0F0F0F]">
            <Header />
            <div className="max-w-[1800px] mx-auto px-4 lg:px-8 grid grid-cols-1 lg:grid-cols-3 gap-8 mt-5">
                {/* Main Content */}
                <div className="lg:col-span-2">
                    {/* Video Player */}
                    <div className="relative rounded-lg mb-4 overflow-hidden">
                        <VideoPlayer
                            isLoading={isLoading}
                            error={error}
                            videoData={data}
                        />
                    </div>

                    {/* Video Info */}
                    <VideoInfo
                        data={data}
                        isLoading={isLoading}
                        error={error}
                    />
                </div>

                {/* Sidebar */}
                <div className="lg:col-span-1">
                    <RecommendedStreams />
                </div>
            </div>
        </div>
    );
};

export default VideoPage;