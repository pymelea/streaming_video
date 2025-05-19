import React from 'react';
import PageError500 from "../components/common/Page500";
import { useGetVideos } from '../hooks/useVideos';
import MainContent from '../components/layout/MainContent';
import Playlists from '../components/video/Playlists';
import LoadingSpinner from '../components/common/LoadingSpinner';

const HomePage = () => {

  const { isLoading, error } = useGetVideos();


  if (error) {
    return <PageError500 />;
  }

  if (isLoading) {
    return <LoadingSpinner />;
  }


  return (
    <div className='min-h-screen bg-[#0F0F0F]'>
      <main className="container mx-auto">
        <MainContent />
        <Playlists />
      </main>
    </div>
  );
};



export default HomePage;
