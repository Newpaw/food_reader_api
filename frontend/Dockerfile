# Use the official Node.js image from the Docker Hub
FROM node:21-slim AS build

# Set the working directory in the container
WORKDIR /app

# Configure npm to bypass proxy issues
RUN npm config set proxy null
RUN npm config set https-proxy null
RUN npm config set strict-ssl false

# Copy the package.json and package-lock.json files
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Use the official Nginx image to serve the build
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
