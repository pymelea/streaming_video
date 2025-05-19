import React from 'react';
import { Link } from 'react-router-dom';
import { List } from 'lucide-react';
import Header from '../components/layout/Header';
import LoadingSpinner from '../components/common/LoadingSpinner';
import PageError500 from '../components/common/Page500';
import { useGetPlaylists } from '../hooks/usePlaylists';

/**
 * PlaylistsPage component displays all available playlists
 */
const PlaylistsPage = () => {
  // Use the hook to fetch playlists
  const { data: playlists = [], isLoading, error } = useGetPlaylists();

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
        <h1 className="text-3xl font-bold text-white mb-8">All Playlists</h1>
        
        {playlists.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-400 text-lg">No playlists available.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {playlists.map((playlist) => (
              <Link
                key={playlist.id}
                to={`/playlist/${playlist.id}`}
                className="bg-[#1A1A1A] rounded-lg overflow-hidden hover:bg-[#252525] transition-all duration-300 group"
              >
                <div className="relative aspect-video bg-[#0F0F0F] flex items-center justify-center">
                  {playlist.thumbnail ? (
                    <img
                      src={playlist.thumbnail}
                      alt={playlist.name}
                      className="w-full h-full object-cover opacity-70"
                    />
                  ) : (
                    <div className="absolute inset-0 bg-gradient-to-br from-purple-900 to-purple-600 opacity-70"></div>
                  )}
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="bg-white/20 backdrop-blur-sm p-4 rounded-full">
                      <List className="w-8 h-8 text-white" />
                    </div>
                  </div>
                  <div className="absolute bottom-3 right-3 bg-black/70 px-2 py-1 rounded text-white text-xs">
                    {playlist?.videos?.length || 0} videos
                  </div>
                </div>
                <div className="p-4">
                  <h3 className="text-white font-medium text-lg mb-2 truncate">{playlist.name}</h3>
                  <p className="text-sm text-gray-400 font-medium line-clamp-2">{playlist.description || 'No description'}</p>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default PlaylistsPage;
