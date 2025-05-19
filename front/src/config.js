/**
 * Application configuration
 */

// Environment-specific configuration
const ENV = import.meta.env.MODE || 'development';

// Base configuration
const config = {
  // API configuration
  api: {
    baseUrl: '/api',
    timeout: 10000, // 10 seconds
    retries: 2,
  },

  // Feature flags
  features: {
    enableMusicSection: true,
    enableRecommendations: true,
    enableDarkMode: true,
  },

  // UI configuration
  ui: {
    defaultTheme: 'dark',
    animationsEnabled: true,
  },
};

// Environment-specific overrides
const envConfig = {
  development: {
    api: {
      baseUrl: 'http://localhost:8000/api',
    },
    debug: true,
  },
  test: {
    api: {
      baseUrl: 'http://localhost:8000/api',
    },
    features: {
      enableRecommendations: false, // Disable in test environment
    },
    debug: true,
  },
  production: {
    api: {
      baseUrl: '/api', // Use relative URL in production
    },
    debug: false,
  },
};

// Merge base config with environment-specific config
const mergedConfig = {
  ...config,
  ...envConfig[ENV],
  api: {
    ...config.api,
    ...(envConfig[ENV]?.api || {}),
  },
  features: {
    ...config.features,
    ...(envConfig[ENV]?.features || {}),
  },
  ui: {
    ...config.ui,
    ...(envConfig[ENV]?.ui || {}),
  },
};

export default mergedConfig;
