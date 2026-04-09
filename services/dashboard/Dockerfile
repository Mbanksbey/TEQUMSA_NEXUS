FROM node:18-slim

WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json* ./
RUN npm ci --only=production

# Copy application code
COPY . ./

# Build the application
RUN npm run build

# Expose the service port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# Run the application
CMD ["npm", "start"]