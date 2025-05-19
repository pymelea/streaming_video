/**
 * Custom hook for accessing the application context
 */
import { useContext } from 'react';
import { AppContext } from './AppProvider';

/**
 * Custom hook to use the app context
 * @returns {Object} App context
 */
const useAppContext = () => {
  const context = useContext(AppContext);
  
  if (!context) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  
  return context;
};

export default useAppContext;
