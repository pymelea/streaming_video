import { describe, it, expect, vi, beforeEach } from 'vitest';
import React from 'react';

// Create mock functions
const renderMock = vi.fn();
const createRootMock = vi.fn(() => ({ render: renderMock }));

// Mock the dependencies
vi.mock('react-dom/client', () => ({
  createRoot: createRootMock
}));

vi.mock('react-router-dom', () => ({
  BrowserRouter: ({ children }) => <div data-testid="browser-router">{children}</div>
}));

vi.mock('@tanstack/react-query', () => ({
  QueryClient: vi.fn(),
  QueryClientProvider: ({ children }) => <div data-testid="query-provider">{children}</div>
}));

vi.mock('@tanstack/react-query-devtools', () => ({
  ReactQueryDevtools: () => <div data-testid="react-query-devtools">DevTools</div>
}));

vi.mock('../App.jsx', () => ({
  default: () => <div data-testid="app-component">App</div>
}));

vi.mock('../index.css', () => ({}));

describe('main.jsx', () => {
  let mockRoot;
  
  beforeEach(() => {
    // Clear all mocks before each test
    vi.clearAllMocks();
    
    // Create a mock DOM element
    mockRoot = document.createElement('div');
    mockRoot.id = 'root';
    document.body.appendChild(mockRoot);
    
    // Mock getElementById
    vi.spyOn(document, 'getElementById').mockImplementation((id) => {
      if (id === 'root') return mockRoot;
      return null;
    });
  });
  
  it('should render the app with all required providers', async () => {
    // Reset mock counts before the test
    createRootMock.mockClear();
    renderMock.mockClear();
    
    // Import the main module which will execute the code
    await import('../main.jsx');
    
    // Check that getElementById was called with 'root'
    expect(document.getElementById).toHaveBeenCalledWith('root');
    
    // Check that createRoot was called with the root element
    expect(createRootMock).toHaveBeenCalledWith(mockRoot);
    
    // Verify that render was called
    expect(renderMock).toHaveBeenCalled();
  });
});
