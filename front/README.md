# StreamTube - Video Streaming Platform

## Overview
StreamTube is a modern video streaming platform built with React and Vite. It provides a clean, responsive interface for browsing and watching videos and music content.

## Project Architecture

The project follows a modular, component-based architecture organized by domain and responsibility:

### Directory Structure

```
/src
  /components
    /video        # Video-related components (VideoPlayer, VideoCard, etc.)
    /music        # Music-related components (MusicContent, etc.)
    /layout       # Layout components (Header, MainContent, etc.)
    /common       # Shared UI components (LoadingSpinner, error pages, etc.)
  /pages          # Page components that compose the application routes
  /hooks          # Custom React hooks for data fetching and logic
  /services       # API service modules for backend communication
  /utils          # Utility functions, constants, and helpers
  /context        # React context providers (if needed)
  /types          # TypeScript type definitions (for future migration)
  /assets         # Static assets (images, icons, etc.)
```

### Design Patterns

- **Container/Presentational Pattern**: Separating data fetching from presentation
- **Custom Hooks**: Encapsulating reusable logic
- **Service Layer**: Abstracting API communication
- **Component Composition**: Building complex UIs from simple components

## Getting Started

### Prerequisites
- Node.js (v14+)
- npm or yarn

### Installation
```bash
npm install
# or
yarn install
```

### Development
```bash
npm run dev
# or
yarn dev
```

### Testing
```bash
npm run test
# or
yarn test
```

### Building for Production
```bash
npm run build
# or
yarn build
```
