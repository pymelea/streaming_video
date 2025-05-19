import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Header from '../layout/Header';

// Mock the Lucide icons
vi.mock('lucide-react', () => ({
  VideoIcon: () => <div data-testid="video-icon">VideoIcon</div>,
  Search: () => <div data-testid="search-icon">Search</div>,
  X: () => <div data-testid="x-icon">X</div>,
  Film: () => <div data-testid="film-icon">Film</div>,
  Play: () => <div data-testid="play-icon">Play</div>
}));

// Wrapper component with Router
const renderWithRouter = (ui) => {
  return render(ui, { wrapper: BrowserRouter });
};

describe('Header', () => {
  it('should render the logo and brand name', () => {
    renderWithRouter(<Header />);
    
    // Check for logo icon
    expect(screen.getByTestId('video-icon')).toBeInTheDocument();
    
    // Check for brand name
    expect(screen.getByText('StreamTube')).toBeInTheDocument();
  });
  
  it('should render the search input', () => {
    renderWithRouter(<Header />);
    
    // Check for search input
    const searchInput = screen.getByPlaceholderText('Search streams or music...');
    expect(searchInput).toBeInTheDocument();
    
    // Check for search button
    expect(screen.getByTestId('search-icon')).toBeInTheDocument();
  });
  
  it('should render the navigation links', () => {
    renderWithRouter(<Header />);
    
    // Check for Videos link
    const videosLink = screen.getByText('Videos');
    expect(videosLink).toBeInTheDocument();
    expect(screen.getByTestId('film-icon')).toBeInTheDocument();
    expect(videosLink.closest('a')).toHaveAttribute('href', '/videos');
    
    // Check for Playlists link
    const playlistsLink = screen.getByText('Playlists');
    expect(playlistsLink).toBeInTheDocument();
    expect(screen.getByTestId('play-icon')).toBeInTheDocument();
    expect(playlistsLink.closest('a')).toHaveAttribute('href', '/playlist');
  });
  
  it('should update search term when typing', () => {
    renderWithRouter(<Header />);
    
    // Get search input
    const searchInput = screen.getByPlaceholderText('Search streams or music...');
    
    // Type in search input
    fireEvent.change(searchInput, { target: { value: 'test search' } });
    
    // Check that input value is updated
    expect(searchInput.value).toBe('test search');
    
    // Check that clear button appears
    expect(screen.getByTestId('x-icon')).toBeInTheDocument();
  });
  
  it('should clear search term when clicking X button', () => {
    renderWithRouter(<Header />);
    
    // Get search input
    const searchInput = screen.getByPlaceholderText('Search streams or music...');
    
    // Type in search input
    fireEvent.change(searchInput, { target: { value: 'test search' } });
    
    // Click the clear button
    const clearButton = screen.getByTestId('x-icon').closest('button');
    fireEvent.click(clearButton);
    
    // Check that input value is cleared
    expect(searchInput.value).toBe('');
  });
  
  it('should call onSearch when form is submitted', () => {
    // Create mock function for onSearch
    const mockOnSearch = vi.fn();
    
    renderWithRouter(<Header onSearch={mockOnSearch} />);
    
    // Get search input and form
    const searchInput = screen.getByPlaceholderText('Search streams or music...');
    const form = searchInput.closest('form');
    
    // Type in search input
    fireEvent.change(searchInput, { target: { value: 'test search' } });
    
    // Submit the form
    fireEvent.submit(form);
    
    // Check that onSearch was called with the search term
    expect(mockOnSearch).toHaveBeenCalledWith('test search');
  });
  
  it('should call onSearch with empty string when clearing search', () => {
    // Create mock function for onSearch
    const mockOnSearch = vi.fn();
    
    renderWithRouter(<Header onSearch={mockOnSearch} />);
    
    // Get search input
    const searchInput = screen.getByPlaceholderText('Search streams or music...');
    
    // Type in search input
    fireEvent.change(searchInput, { target: { value: 'test search' } });
    
    // Click the clear button
    const clearButton = screen.getByTestId('x-icon').closest('button');
    fireEvent.click(clearButton);
    
    // Check that onSearch was called with empty string
    expect(mockOnSearch).toHaveBeenCalledWith('');
  });
});
