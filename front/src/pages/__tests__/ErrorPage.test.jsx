import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';

import ErrorPage from '../ErrorPage';

// Mock the Page500 component
vi.mock('../../components/common/Page500', () => ({
  default: vi.fn(() => <div data-testid="error-page">Error Page</div>)
}));

describe('ErrorPage', () => {
  it('should render the Page500 component', () => {
    // Render the component
    render(<ErrorPage />);

    // Check that the Page500 component is rendered
    expect(screen.getByTestId('error-page')).toBeInTheDocument();
    expect(screen.getByText('Error Page')).toBeInTheDocument();
  });
});
