import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import React from 'react';

import { useGetVideos, useGetVideo } from '../useVideos.jsx';
import * as videosService from '../../services/videoService';

// Mock the video service
vi.mock('../../services/videoService', () => ({
  getVideos: vi.fn(),
  getVideo: vi.fn()
}));

// Create a wrapper with QueryClientProvider for testing hooks
const createWrapper = () => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        // Turn off retries for testing
        retry: false,
        // Don't cache for testing
        cacheTime: 0,
        // Don't refetch on window focus for testing
        refetchOnWindowFocus: false
      }
    }
  });

  return ({ children }) => (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
};

describe('useVideos hooks', () => {
  let wrapper;

  beforeEach(() => {
    vi.resetAllMocks();
    wrapper = createWrapper();
  });

  describe('useGetVideos', () => {
    it('should return videos data when successful', async () => {
      // Mock data
      const mockVideos = [
        { id: 1, title: 'Test Video 1', stream_url: '/api/videos/stream/1' },
        { id: 2, title: 'Test Video 2', stream_url: '/api/videos/stream/2' }
      ];

      // Setup mock implementation
      videosService.getVideos.mockResolvedValue(mockVideos);

      // Render the hook
      const { result } = renderHook(() => useGetVideos(), { wrapper });

      // Initially, it should be loading
      expect(result.current.isLoading).toBe(true);
      expect(result.current.data).toBeUndefined();

      // Wait for the query to resolve
      await waitFor(() => expect(result.current.isSuccess).toBe(true));

      // Check the result
      expect(result.current.data).toEqual(mockVideos);
      expect(videosService.getVideos).toHaveBeenCalledTimes(1);
    });

    it('should handle error state', async () => {
      // Setup mock implementation to return undefined (error case)
      const consoleSpy = vi.spyOn(console, 'error');
      videosService.getVideos.mockResolvedValue(undefined);

      // Render the hook
      const { result } = renderHook(() => useGetVideos(), { wrapper });

      // Wait for the query to complete
      await waitFor(() => expect(result.current.isLoading).toBe(false));

      // Check the result
      expect(result.current.data).toBeUndefined();
      expect(consoleSpy).toHaveBeenCalled();
      expect(videosService.getVideos).toHaveBeenCalledTimes(1);
    });
  });

  describe('useGetVideo', () => {
    it('should return video data when successful', async () => {
      // Mock data
      const mockVideo = { 
        id: 1, 
        title: 'Test Video', 
        stream_url: '/api/videos/stream/1',
        subtitles_urls: ['/subtitles/content/1']
      };

      // Setup mock implementation
      videosService.getVideo.mockResolvedValue(mockVideo);

      // Render the hook with an ID
      const { result } = renderHook(() => useGetVideo(1), { wrapper });

      // Initially, it should be loading
      expect(result.current.isLoading).toBe(true);
      expect(result.current.data).toBeUndefined();

      // Wait for the query to resolve
      await waitFor(() => expect(result.current.isSuccess).toBe(true));

      // Check the result
      expect(result.current.data).toEqual(mockVideo);
      expect(videosService.getVideo).toHaveBeenCalledTimes(1);
      expect(videosService.getVideo).toHaveBeenCalledWith(1);
    });

    it('should not fetch when id is not provided', async () => {
      // Render the hook without an ID
      const { result } = renderHook(() => useGetVideo(null), { wrapper });

      // The query should be disabled
      expect(result.current.isLoading).toBe(false);
      expect(result.current.isFetching).toBe(false);
      expect(result.current.data).toBeUndefined();

      // Service should not be called
      expect(videosService.getVideo).not.toHaveBeenCalled();
    });

    it('should handle error state', async () => {
      // Setup mock implementation to return undefined (error case)
      const consoleSpy = vi.spyOn(console, 'error');
      videosService.getVideo.mockResolvedValue(undefined);

      // Render the hook with an ID
      const { result } = renderHook(() => useGetVideo(1), { wrapper });

      // Wait for the query to complete
      await waitFor(() => expect(result.current.isLoading).toBe(false));

      // Check the result
      expect(result.current.data).toBeUndefined();
      expect(consoleSpy).toHaveBeenCalled();
      expect(videosService.getVideo).toHaveBeenCalledTimes(1);
    });
  });
});
