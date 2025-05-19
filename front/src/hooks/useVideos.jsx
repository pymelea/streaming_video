/**
 * Custom hooks for video data fetching using React Query
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getVideos, getVideo, likeVideo } from '../services/videoService';

/**
 * Hook to fetch all videos
 * @returns {Object} Query result with data, loading state, and error
 */
export const useGetVideos = () => {
  return useQuery({
    queryKey: ['videos'],
    queryFn: getVideos,
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 2,
  });
};

/**
 * Hook to fetch a specific video by ID
 * @param {string} id - Video ID
 * @returns {Object} Query result with data, loading state, and error
 */
export const useGetVideo = (id) => {
  return useQuery({
    queryKey: ['video', id],
    queryFn: () => getVideo(id),
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 2,
    enabled: !!id, // Only run the query if we have an ID
  });
};

/**
 * Hook to like a video
 * @returns {Object} Mutation result with mutate function, loading state, and error
 */
export const useLikeVideo = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (id) => likeVideo(id),
    onSuccess: (data, variables) => {
      // Update the cache for this specific video
      queryClient.invalidateQueries({ queryKey: ['video', variables] });
      // Optionally update the videos list
      queryClient.invalidateQueries({ queryKey: ['videos'] });
    },
  });
};

/**
 * Hook to get recommended videos based on a video ID
 * @param {string} id - Video ID to base recommendations on
 * @returns {Object} Query result with data, loading state, and error
 */
export const useGetRecommendedVideos = (id) => {
  return useQuery({
    queryKey: ['videos', 'recommended', id],
    queryFn: async () => {
      // For now, we'll just return all videos as recommendations
      // In a real app, this would call a specific API endpoint
      const videos = await getVideos();
      return videos?.filter(video => video.id !== id) || [];
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: 2,
    enabled: !!id, // Only run the query if we have an ID
  });
};
