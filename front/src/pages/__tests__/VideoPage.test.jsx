import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MemoryRouter, Routes, Route } from 'react-router-dom';

import VideoPage from '../VideoPage';

// Mock the hooks
const mockUseGetVideo = vi.fn();
const mockUseGetRecommendedVideos = vi.fn();

vi.mock('../../hooks/useVideos', () => ({
  useGetVideo: () => mockUseGetVideo(),
  useGetRecommendedVideos: () => mockUseGetRecommendedVideos()
}));

// Mock the components
const VideoPlayerMock = vi.fn(() => <div data-testid="video-player">Video Player</div>);
const VideoInfoMock = vi.fn(() => <div data-testid="video-info">Video Info</div>);
const RecommendedStreamsMock = vi.fn(() => <div data-testid="recommended-streams">Recommended Streams</div>);
const HeaderMock = vi.fn(() => <div data-testid="header">Header</div>);

vi.mock('../../components/video/VideoPlayer', () => ({
  default: (props) => {
    VideoPlayerMock(props);
    return <div data-testid="video-player">Video Player</div>;
  }
}));

vi.mock('../../components/video/VideoInfo', () => ({
  default: (props) => {
    VideoInfoMock(props);
    return <div data-testid="video-info">Video Info</div>;
  }
}));

vi.mock('../../components/video/RecommendedStreams', () => ({
  default: () => <div data-testid="recommended-streams">Recommended Streams</div>
}));

vi.mock('../../components/layout/Header', () => ({
  default: () => <div data-testid="header">Header</div>
}));

// Create a wrapper with QueryClientProvider and Router for testing
const createWrapper = (initialEntries = ["/video/1"]) => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
        cacheTime: 0,
        refetchOnWindowFocus: false
      }
    }
  });

  return ({ children }) => (
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={initialEntries}>
        <Routes>
          <Route path="/video/:id" element={children} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>
  );
};

describe('VideoPage', () => {
  let wrapper;

  beforeEach(() => {
    vi.resetAllMocks();
    wrapper = createWrapper();
  });

  it('should render loading state correctly', () => {
    // Mock loading state
    mockUseGetVideo.mockReturnValue({
      isLoading: true,
      error: null,
      data: null
    });
    
    mockUseGetRecommendedVideos.mockReturnValue({
      isLoading: false,
      error: null,
      data: []
    });

    // Render the component
    render(<VideoPage />, { wrapper });

    // Check that components are rendered correctly
    expect(screen.getByTestId('header')).toBeInTheDocument();
    expect(screen.getByTestId('video-player')).toBeInTheDocument();
    expect(screen.getByTestId('video-info')).toBeInTheDocument();
    expect(screen.getByTestId('recommended-streams')).toBeInTheDocument();
  });

  it('should render error state correctly', () => {
    // Mock error state
    const error = new Error('Failed to fetch video');
    mockUseGetVideo.mockReturnValue({
      isLoading: false,
      error,
      data: null
    });
    
    mockUseGetRecommendedVideos.mockReturnValue({
      isLoading: false,
      error: null,
      data: []
    });

    // Render the component
    render(<VideoPage />, { wrapper });

    // Check that components are rendered correctly
    expect(screen.getByTestId('header')).toBeInTheDocument();
    expect(screen.getByTestId('video-player')).toBeInTheDocument();
    expect(screen.getByTestId('video-info')).toBeInTheDocument();
    expect(screen.getByTestId('recommended-streams')).toBeInTheDocument();
  });

  it('should render video data correctly', () => {
    // Mock successful state with data
    const mockVideo = {
      id: 1,
      title: 'Test Video',
      stream_url: '/api/videos/stream/1',
      subtitles_urls: ['/subtitles/content/1']
    };

    mockUseGetVideo.mockReturnValue({
      isLoading: false,
      error: null,
      data: mockVideo
    });
    
    mockUseGetRecommendedVideos.mockReturnValue({
      isLoading: false,
      error: null,
      data: []
    });

    // Render the component
    render(<VideoPage />, { wrapper });

    // Check that components are rendered correctly
    expect(screen.getByTestId('header')).toBeInTheDocument();
    expect(screen.getByTestId('video-player')).toBeInTheDocument();
    expect(screen.getByTestId('video-info')).toBeInTheDocument();
    expect(screen.getByTestId('recommended-streams')).toBeInTheDocument();
  });

  it('should pass correct props to child components', () => {
    // Reset mocks before the test
    VideoPlayerMock.mockClear();
    VideoInfoMock.mockClear();
    
    // Mock successful state with data
    const mockVideo = {
      id: 1,
      title: 'Test Video',
      stream_url: '/api/videos/stream/1',
      subtitles_urls: ['/subtitles/content/1']
    };

    mockUseGetVideo.mockReturnValue({
      isLoading: false,
      error: null,
      data: mockVideo
    });
    
    // Mock recommended videos data
    mockUseGetRecommendedVideos.mockReturnValue({
      isLoading: false,
      error: null,
      data: []
    });

    // Render the component
    render(<VideoPage />, { wrapper });

    // Check that the components are rendered
    expect(screen.getByTestId('video-player')).toBeInTheDocument();
    expect(screen.getByTestId('video-info')).toBeInTheDocument();
    
    // Check that the components received the correct props
    expect(VideoPlayerMock).toHaveBeenCalledWith(
      expect.objectContaining({
        videoData: mockVideo,
        isLoading: false,
        error: null
      })
    );

    expect(VideoInfoMock).toHaveBeenCalledWith(
      expect.objectContaining({
        data: mockVideo,
        isLoading: false,
        error: null
      })
    );
  });
});
