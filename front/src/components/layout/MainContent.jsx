import React, { useState, useEffect } from 'react';
import { useGetVideos } from '../../hooks/useVideos';
import { Link } from 'react-router-dom';
import Header from './Header';


const MainContent = () => {
    const { data } = useGetVideos();
    const [searchTerm, setSearchTerm] = useState('');
    const [filteredVideos, setFilteredVideos] = useState([]);

    useEffect(() => {
        if (data) {
            setFilteredVideos(data);
        }
    }, [data]);

    const handleSearch = (term) => {
        setSearchTerm(term);
        if (!term.trim()) {
            setFilteredVideos(data);
            return;
        }

        const filtered = data.filter(video =>
            video.title?.toLowerCase().includes(term.toLowerCase()) ||
            video.streamer?.toLowerCase().includes(term.toLowerCase()) ||
            video.category?.toLowerCase().includes(term.toLowerCase())
        );
        setFilteredVideos(filtered);
    };

    return (
        <main className="pt-14 pb-20">
            <Header onSearch={handleSearch} />

            <div className="px-8 mt-4">
                {searchTerm && (
                    <div className="mb-4">
                        <p className="text-white">
                            {filteredVideos.length} {filteredVideos.length === 1 ? 'result' : 'results'} for <span className="font-bold">"{searchTerm}"</span>
                        </p>
                    </div>
                )}

                <h2 className="text-2xl font-bold text-white mb-4">{searchTerm ? 'Search Results' : 'Videos'}</h2>

                {filteredVideos.length === 0 ? (
                    <div className="text-center py-10">
                        <p className="text-gray-400 text-lg">No videos found matching your search.</p>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                        {filteredVideos.map((video) => (
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
                                            <span className="px-2 py-1 bg-red-600 text-white text-sm rounded">{video.categories.join(', ') ?? "HOME"}</span>
                                        </div>
                                    </div>
                                </div>
                                <div className="p-4">
                                    <h3 className="text-white font-medium text-lg mb-2 truncate">{video.title}</h3>
                                    <div className="flex items-center justify-between">
                                        <p className="text-sm text-gray-400 font-medium">{video.year ?? "Unknown Year"}</p>
                                        <span className="text-xs text-purple-400">{video.duration ? `${Math.floor(video.duration / 60)}h ${video.duration % 60}m` : "00:00"}</span>
                                    </div>
                                </div>
                            </Link>
                        ))}
                    </div>
                )}
            </div>
        </main>
    );
};

export default MainContent;