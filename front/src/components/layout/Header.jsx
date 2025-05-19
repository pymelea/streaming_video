import { VideoIcon, Search, X, Play, Film } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useState } from 'react';

const Header = ({ onSearch }) => {
  const [searchTerm, setSearchTerm] = useState('');
  
  const handleSearch = (e) => {
    e.preventDefault();
    if (onSearch) {
      onSearch(searchTerm);
    }
  };
  return (
    <header className="fixed top-0 left-0 right-0 bg-[#1A1A1A] border-b border-[#252525] z-50">
      <div className="flex items-center justify-between px-4 h-14">
        {/* Left section */}
        <div className="flex items-center">
          <Link to="/">
            <div className="flex items-center cursor-pointer">
              <VideoIcon className="w-8 h-8 text-purple-600" />
              <span className="text-xl text-white font-bold ml-2">StreamTube</span>
            </div>
          </Link>
        </div>

        {/* Middle section - Search */}
        <div className="hidden md:flex items-center flex-1 max-w-2xl mx-4">
          <form onSubmit={handleSearch} className="flex flex-1 relative">
            <input
              type="text"
              placeholder="Search streams or music..."
              className="w-full px-4 py-2 bg-[#252525] border border-[#333333] rounded-l-full focus:outline-none focus:border-purple-500 text-white placeholder-gray-400"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            {searchTerm && (
              <button
                type="button"
                onClick={() => {
                  setSearchTerm('');
                  if (onSearch) onSearch('');
                }}
                className="absolute right-20 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-white transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            )}
            <button 
              type="submit"
              className="px-6 bg-[#333333] border border-l-0 border-[#333333] rounded-r-full hover:bg-[#404040] transition-colors text-gray-300 hover:text-white"
            >
              <Search className="w-5 h-5" />
            </button>
          </form>
        </div>

        {/* Right section */}
        <div className="flex items-center space-x-4">
          <Link to="/videos" className="flex items-center text-gray-300 hover:text-white transition-colors">
            <Film className="w-5 h-5 mr-1" />
            <span className="hidden sm:inline">Videos</span>
          </Link>
          <Link to="/playlist" className="flex items-center text-purple-600 hover:text-purple-500 transition-colors">
            <Play className="w-5 h-5 mr-1" />
            <span className="hidden sm:inline">Playlists</span>
          </Link>
        </div>
      </div>
    </header>
  );
};

export default Header;