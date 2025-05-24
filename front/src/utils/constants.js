/**
 * Application constants
 */

// API endpoints
export const API_ENDPOINTS = {
  VIDEOS: '/videos/',
  VIDEO: (id) => `/videos/${id}`,
  VIDEO_STREAM: (id) => `/videos/${id}/stream/`,
  PLAYLISTS: '/playlists/',
  PLAYLIST: (id) => `/playlists/${id}`,
  PLAYLIST_VIDEOS: (id) => `/playlists/${id}/videos/`,
};

// Application routes
export const ROUTES = {
  HOME: '/',
  VIDEO: (id) => `/video/${id}`,
  ERROR: '/error',
};

// UI constants
export const UI = {
  BREAKPOINTS: {
    SM: 640,
    MD: 768,
    LG: 1024,
    XL: 1280,
  },
  COLORS: {
    PRIMARY: '#0F0F0F',
    SECONDARY: '#1A1A1A',
    ACCENT: '#FF0000',
    TEXT: '#FFFFFF',
    TEXT_SECONDARY: '#AAAAAA',
  },
};
