import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from '../App';

// Mock the page components
vi.mock('../pages/HomePage', () => ({
  default: () => <div data-testid="home-page">Home Page</div>
}));

vi.mock('../pages/ErrorPage', () => ({
  default: () => <div data-testid="error-page">Error Page</div>
}));

vi.mock('../pages/VideoPage', () => ({
  default: () => <div data-testid="video-page">Video Page</div>
}));

vi.mock('../components/common/Page404', () => ({
  default: () => <div data-testid="page-404">404 Page</div>
}));

// Helper function to render with router
const renderWithRouter = (ui, { route = '/' } = {}) => {
  return render(
    <MemoryRouter initialEntries={[route]}>
      {ui}
    </MemoryRouter>
  );
};

describe('App', () => {
  it('should render HomePage on the root route', () => {
    renderWithRouter(<App />, { route: '/' });
    expect(screen.getByTestId('home-page')).toBeInTheDocument();
  });

  it('should render ErrorPage on the /error route', () => {
    renderWithRouter(<App />, { route: '/error' });
    expect(screen.getByTestId('error-page')).toBeInTheDocument();
  });

  it('should render VideoPage on the /video/:id route', () => {
    renderWithRouter(<App />, { route: '/video/123' });
    expect(screen.getByTestId('video-page')).toBeInTheDocument();
  });

  it('should render 404 page for unknown routes', () => {
    renderWithRouter(<App />, { route: '/unknown-route' });
    expect(screen.getByTestId('page-404')).toBeInTheDocument();
  });
});
