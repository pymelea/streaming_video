# Build stage
FROM node:18-alpine as build

WORKDIR /app

# Create a non-root user
RUN addgroup -S nodegroup && adduser -S nodeuser -G nodegroup

# Install pnpm
RUN npm install -g pnpm

# Copy package.json and lock files
COPY package.json pnpm-lock.yaml ./

# Set proper ownership
RUN chown -R nodeuser:nodegroup /app

# Switch to non-root user
USER nodeuser

# Install dependencies
RUN pnpm install --frozen-lockfile

# Copy the rest of the code
COPY --chown=nodeuser:nodegroup . .

# Build the application
RUN pnpm build

# Production stage
FROM nginx:alpine

# Copy built files from the build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
