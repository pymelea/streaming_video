import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

import HomePage from '../HomePage';
import { useGetVideos } from '../../hooks/useVideos';
import { useGetPlaylists } from '../../hooks/usePlaylists';

// Mock the hooks
vi.mock('../../hooks/useVideos', () => ({
  useGetVideos: vi.fn()
}));

vi.mock('../../hooks/usePlaylists', () => ({
  useGetPlaylists: vi.fn()
}));

// Mock the components
vi.mock('../../components/common/Page500', () => ({
  default: vi.fn(() => <div data-testid="error-page">Error Page</div>)
}));

vi.mock('../../components/common/LoadingSpinner', () => ({
  default: vi.fn(() => <div data-testid="loading-spinner">Loading...</div>)
}));

vi.mock('../../components/layout/MainContent', () => ({
  default: vi.fn(() => <div data-testid="main-content">Main Content</div>)
}));

vi.mock('../../components/video/Playlists', () => ({
  default: vi.fn(() => <div data-testid="playlists-component">Playlists</div>)
}));

// Create a wrapper with QueryClientProvider for testing
const createWrapper = () => {
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
      {children}
    </QueryClientProvider>
  );
};

describe('HomePage', () => {
  let wrapper;

  beforeEach(() => {
    vi.resetAllMocks();
    wrapper = createWrapper();
  });

  it('should render loading state correctly', () => {
    // Mock loading state
    useGetVideos.mockReturnValue({
      isLoading: true,
      error: null,
      data: null
    });
    
    useGetPlaylists.mockReturnValue({
      isLoading: false,
      error: null,
      data: []
    });

    // Render the component
    render(<HomePage />, { wrapper });

    // Check that loading spinner is shown
    expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();
    
    // Check that other components are not rendered
    expect(screen.queryByTestId('error-page')).not.toBeInTheDocument();
    expect(screen.queryByTestId('main-content')).not.toBeInTheDocument();
    expect(screen.queryByTestId('playlists-component')).not.toBeInTheDocument();
  });

  it('should render error state correctly', () => {
    // Mock error state
    const error = new Error('Failed to fetch videos');
    useGetVideos.mockReturnValue({
      isLoading: false,
      error,
      data: null
    });
    
    useGetPlaylists.mockReturnValue({
      isLoading: false,
      error: null,
      data: []
    });

    // Render the component
    render(<HomePage />, { wrapper });

    // Check that error page is shown
    expect(screen.getByTestId('error-page')).toBeInTheDocument();
    
    // Check that other components are not rendered
    expect(screen.queryByTestId('loading-spinner')).not.toBeInTheDocument();
    expect(screen.queryByTestId('main-content')).not.toBeInTheDocument();
    expect(screen.queryByTestId('playlists-component')).not.toBeInTheDocument();
  });

  it('should render content when data is loaded', () => {
    // Mock successful state with data
    const mockVideos = [
      { id: 1, title: 'Test Video 1' },
      { id: 2, title: 'Test Video 2' }
    ];
    
    const mockPlaylists = [
      { id: 1, name: 'Test Playlist 1' },
      { id: 2, name: 'Test Playlist 2' }
    ];

    useGetVideos.mockReturnValue({
      isLoading: false,
      error: null,
      data: mockVideos
    });
    
    useGetPlaylists.mockReturnValue({
      isLoading: false,
      error: null,
      data: mockPlaylists
    });

    // Render the component
    render(<HomePage />, { wrapper });

    // Check that content components are rendered
    expect(screen.getByTestId('main-content')).toBeInTheDocument();
    expect(screen.getByTestId('playlists-component')).toBeInTheDocument();
    
    // Check that other components are not rendered
    expect(screen.queryByTestId('loading-spinner')).not.toBeInTheDocument();
    expect(screen.queryByTestId('error-page')).not.toBeInTheDocument();
  });

  it('should accept and use headerTitle prop', () => {
    // Mock successful state with data
    useGetVideos.mockReturnValue({
      isLoading: false,
      error: null,
      data: [{ id: 1, title: 'Test Video' }]
    });
    
    useGetPlaylists.mockReturnValue({
      isLoading: false,
      error: null,
      data: [{ id: 1, name: 'Test Playlist' }]
    });

    // Render the component with custom header title
    const customTitle = 'Custom Title';
    render(<HomePage headerTitle={customTitle} />, { wrapper });

    // Check that content is rendered correctly
    expect(screen.getByTestId('main-content')).toBeInTheDocument();
    expect(screen.getByTestId('playlists-component')).toBeInTheDocument();
  });
});
