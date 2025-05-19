import React from 'react';
import { Link } from 'react-router-dom';
import { List, Play } from 'lucide-react';
import { useGetPlaylists } from '../../hooks/usePlaylists';
import LoadingSpinner from '../common/LoadingSpinner';

/**
 * Component to display all available playlists
 */
const Playlists = () => {
  const { data: playlists = [], isLoading, error } = useGetPlaylists();

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-8">
        <LoadingSpinner />
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-red-500 p-4 bg-red-100 rounded">
        Error loading playlists. Please try again later.
      </div>
    );
  }

  if (playlists.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-400 text-lg">No playlists available.</p>
      </div>
    );
  }

  return (
    <div className="mt-12 pb-12">
      <h2 className="text-2xl font-bold text-white mb-6">Playlists</h2>
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
                {playlist?.videos?.length} videos
              </div>
            </div>
            <div className="p-4">
              <h3 className="text-white font-medium text-lg mb-2 truncate">{playlist.name}</h3>
              <div className="flex items-center justify-between">
                <p className="text-sm text-gray-400 font-medium truncate flex-1">{playlist.description || 'No description'}</p>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default Playlists;
