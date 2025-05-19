/**
 * Custom hooks for playlist data fetching using React Query
 */
import { useQuery } from '@tanstack/react-query';
import { getPlaylists, getPlaylist, getPlaylistVideos } from '../services/playlistService';

/**
 * Hook to fetch all playlists
 * @returns {Object} Query result with data, loading state, and error
 */
export const useGetPlaylists = () => {
  return useQuery({
    queryKey: ['playlists'],
    queryFn: getPlaylists,
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 2,
  });
};

/**
 * Hook to fetch a specific playlist by ID
 * @param {string} id - Playlist ID
 * @returns {Object} Query result with data, loading state, and error
 */
export const useGetPlaylist = (id) => {
  return useQuery({
    queryKey: ['playlist', id],
    queryFn: () => getPlaylist(id),
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 2,
    enabled: !!id, // Only run the query if we have an ID
  });
};

/**
 * Hook to fetch videos in a specific playlist
 * @param {string} id - Playlist ID
 * @returns {Object} Query result with data, loading state, and error
 */
export const useGetPlaylistVideos = (id) => {
  return useQuery({
    queryKey: ['playlist', id, 'videos'],
    queryFn: () => getPlaylistVideos(id),
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 2,
    enabled: !!id, // Only run the query if we have an ID
  });
};
