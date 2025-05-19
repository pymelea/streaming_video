/**
 * Playlist service for handling playlist-related API calls
 */
import { API_ENDPOINTS } from '../utils/constants';
import { get } from '../utils/api';

/**
 * Get all playlists
 * @returns {Promise<Array>} List of playlists
 */
export const getPlaylists = async () => {
  try {
    return await get(API_ENDPOINTS.PLAYLISTS);
  } catch (error) {
    if (error.name === 'AbortError') {
      console.log('Request was aborted');
    } else {
      console.error('Error fetching playlists:', error);
    }
    throw error;
  }
};

/**
 * Get a specific playlist by ID
 * @param {string} id - Playlist ID
 * @param {AbortSignal} signal - Optional AbortSignal for cancellation
 * @returns {Promise<Object>} Playlist data
 */
export const getPlaylist = async (id, signal) => {
  try {
    const options = signal ? { signal } : {};
    return await get(API_ENDPOINTS.PLAYLIST(id), options);
  } catch (error) {
    if (error.name === 'AbortError') {
      console.log('Request was aborted');
    } else {
      console.error('Error fetching playlist:', error);
    }
    throw error;
  }
};

/**
 * Get videos in a specific playlist
 * @param {string} id - Playlist ID
 * @param {AbortSignal} signal - Optional AbortSignal for cancellation
 * @returns {Promise<Array>} List of videos in the playlist
 */
export const getPlaylistVideos = async (id, signal) => {
  try {
    const options = signal ? { signal } : {};
    return await get(API_ENDPOINTS.PLAYLIST_VIDEOS(id), options);
  } catch (error) {
    if (error.name === 'AbortError') {
      console.log('Request was aborted');
    } else {
      console.error('Error fetching playlist videos:', error);
    }
    throw error;
  }
};
