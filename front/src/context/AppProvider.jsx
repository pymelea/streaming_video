/**
 * Application context provider for global state management
 */
import React, { createContext, useState, useCallback, useMemo } from 'react';
import PropTypes from 'prop-types';
import config from '../config';

// Create context
export const AppContext = createContext();

/**
 * Application context provider
 * @param {Object} props - Component props
 * @returns {JSX.Element} Provider component
 */
const AppProvider = ({ children }) => {
  // Theme state (light/dark)
  const [theme, setTheme] = useState(config.ui.defaultTheme);
  
  // User preferences
  const [preferences, setPreferences] = useState({
    autoplay: true,
    notifications: true,
    quality: 'auto',
  });
  
  // Toggle theme function
  const toggleTheme = useCallback(() => {
    setTheme(prevTheme => (prevTheme === 'dark' ? 'light' : 'dark'));
  }, []);
  
  // Update preferences function
  const updatePreferences = useCallback((newPreferences) => {
    setPreferences(prev => ({
      ...prev,
      ...newPreferences,
    }));
  }, []);
  
  // Memoize context value to prevent unnecessary re-renders
  const contextValue = useMemo(() => ({
    theme,
    toggleTheme,
    preferences,
    updatePreferences,
    features: config.features,
  }), [theme, toggleTheme, preferences, updatePreferences]);
  
  return (
    <AppContext.Provider value={contextValue}>
      {children}
    </AppContext.Provider>
  );
};

AppProvider.propTypes = {
  children: PropTypes.node.isRequired,
};

export default AppProvider;
