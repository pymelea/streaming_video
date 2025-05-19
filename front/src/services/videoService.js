/**
 * Video service for handling video-related API calls
 */
import { get } from '../utils/api';
import { API_ENDPOINTS } from '../utils/constants';
import config from '../config';

/**
 * Get all videos
 * @returns {Promise<Array>} List of videos
 */
export const getVideos = async () => {
  try {
    return await get(API_ENDPOINTS.VIDEOS);
  } catch (error) {
    console.error('Error fetching videos:', error);
    return undefined;
  }
};

/**
 * Get a specific video by ID
 * @param {string} id - Video ID
 * @returns {Promise<Object>} Video data
 */
export const getVideo = async (id) => {
  try {
    return await get(API_ENDPOINTS.VIDEO(id));
  } catch (error) {
    console.error(`Error fetching video ${id}:`, error);
    return undefined;
  }
};

/**
 * Get the stream URL for a video
 * @param {string} videoId - Video ID
 * @returns {string} Full stream URL
 */
export const getStreamUrl = (videoId) => {
  return `${config.api.baseUrl}${API_ENDPOINTS.VIDEO_STREAM(videoId)}`;
};

/**
 * Like a video
 * @param {string} id - Video ID
 * @returns {Promise<Object>} Updated video data
 */
export const likeVideo = async (id) => {
  try {
    return await get(`/videos/${id}/like`);
  } catch (error) {
    console.error(`Error liking video ${id}:`, error);
    return undefined;
  }
};
