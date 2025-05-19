/**
 * Application context for global state management
 */
import React, { createContext, useContext, useState, useCallback, useMemo } from 'react';
import PropTypes from 'prop-types';
import config from '../config';

// Create context
const AppContext = createContext();

/**
 * Application context provider
 * @param {Object} props - Component props
 * @returns {JSX.Element} Provider component
 */
export const AppProvider = ({ children }) => {
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

/**
 * Custom hook to use the app context
 * @returns {Object} App context
 */
export const useAppContext = () => {
  const context = useContext(AppContext);
  
  if (!context) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  
  return context;
};
