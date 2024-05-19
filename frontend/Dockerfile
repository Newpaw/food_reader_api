# Stage 1: Build the React application
FROM node:21-slim AS build

# Set the working directory in the container
WORKDIR /app

# Configure npm to bypass proxy issues
RUN npm config set proxy null
RUN npm config set https-proxy null
RUN npm config set strict-ssl false

# Copy the package.json and package-lock.json files
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the application code into the container
COPY . .

# Build the application
RUN npm run build

# Stage 2: Serve the React application with Nginx
FROM nginx:alpine

# Copy the build output from the previous stage
COPY --from=build /app/build /usr/share/nginx/html

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
