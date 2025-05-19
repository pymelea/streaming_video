import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import VideoInfo from '../video/VideoInfo';

// Mock the components
vi.mock('../../components/common/Page500', () => ({
  default: vi.fn(() => <div data-testid="error-page">Error Page</div>)
}));

vi.mock('../../components/common/LoadingSpinner', () => ({
  default: vi.fn(() => <div data-testid="loading-spinner">Loading...</div>)
}));

describe('VideoInfo', () => {
  it('should render loading state correctly', () => {
    render(<VideoInfo isLoading={true} error={null} data={null} />);
    
    // Check that loading spinner is shown
    expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();
  });
  
  it('should render error state correctly', () => {
    const error = new Error('Failed to fetch video');
    render(<VideoInfo isLoading={false} error={error} data={null} />);
    
    // Check that error page is shown
    expect(screen.getByTestId('error-page')).toBeInTheDocument();
  });
  
  it('should render video information correctly', () => {
    const mockVideo = {
      id: '1',
      title: 'Test Video Title',
      categories: ['Action', 'Drama'],
      year: '2023',
      description: 'This is a test video description'
    };
    
    render(<VideoInfo isLoading={false} error={null} data={mockVideo} />);
    
    // Check that the title is displayed
    expect(screen.getByText(mockVideo.title)).toBeInTheDocument();
    
    // Check for categories
    expect(screen.getByText('Action, Drama')).toBeInTheDocument();
    
    // Check for year
    expect(screen.getByText('Year 2023')).toBeInTheDocument();
    
    // Check for description
    expect(screen.getByText(mockVideo.description)).toBeInTheDocument();
  });
  
  it('should handle missing data gracefully', () => {
    const mockVideo = {
      id: '1',
      title: 'Test Video Title',
      // Missing categories and year
      description: null // No description
    };
    
    render(<VideoInfo isLoading={false} error={null} data={mockVideo} />);
    
    // Check that the title is displayed
    expect(screen.getByText(mockVideo.title)).toBeInTheDocument();
    
    // Check for fallback text
    expect(screen.getByText('No description available')).toBeInTheDocument();
  });
});
