import React from 'react';
import { WrenchIcon, Home } from 'lucide-react';

const PageError404 = ({
  onRetry = () => window.location.reload(),
  onHome = () => window.location.href = '/'
}) => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-[#F9F9F9] px-4 py-8">
      <div className="max-w-lg w-full">

        <div className="flex justify-center mb-8">
          <div className="relative flex items-center transform hover:scale-105 transition-transform duration-300">
            <span className="text-2xl font-bold px-4 py-1 bg-red-600 text-white rounded-lg shadow-lg hover:bg-red-700 transition-colors duration-300">StreamTube</span>
          </div>
        </div>


        <div className="flex justify-center mb-6">
          <div className="bg-gray-100 p-5 rounded-full shadow-md hover:shadow-lg transition-shadow duration-300 group">
            <WrenchIcon size={48} className="text-gray-600 group-hover:rotate-180 transition-transform duration-700" />
          </div>
        </div>


        <div className="text-center mb-8 transform hover:-translate-y-1 transition-transform duration-300">
          <h1 className="text-xl font-bold text-gray-900 mb-2">
            404 Page Not Found
          </h1>
          <p className="text-gray-700 mb-4 hover:text-gray-900 transition-colors duration-300">
            Sorry, something went wrong. A team of highly trained monkeys has been dispatched to deal with this situation.
          </p>
          <p className="text-sm text-gray-600">
            If you see them, show them this information:
            <span className="block mt-2 font-mono bg-gray-100 p-2 rounded text-xs hover:bg-gray-200 transition-colors duration-300 cursor-pointer">
              Error 404 (Page Not Found)
            </span>
          </p>
        </div>


        <div className="flex flex-col sm:flex-row justify-center space-y-2 sm:space-y-0 sm:space-x-3">
          <button
            onClick={onRetry}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-full font-medium transition-all duration-300 transform hover:scale-105 hover:shadow-lg active:scale-95"
          >
            Try Again
          </button>
          <button
            onClick={onHome}
            className="flex items-center justify-center bg-gray-100 hover:bg-gray-200 text-gray-800 px-6 py-2 rounded-full font-medium transition-all duration-300 transform hover:scale-105 hover:shadow-lg active:scale-95"
          >
            <Home size={16} className="mr-2" />
            Go Home
          </button>
        </div>
      </div>


      <div className="mt-16 text-xs text-gray-500 hover:text-gray-700 transition-colors duration-300">
        © 2025 StreamTube and the StreamTube logo are registered trademarks of StreamTube.
      </div>
    </div>
  );
};

export default PageError404;