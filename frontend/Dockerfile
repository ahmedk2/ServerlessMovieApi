FROM nginx:stable

WORKDIR /usr/share/nginx/html

# Copy the HTML, CSS, and JavaScript files into the container
COPY . ./

EXPOSE 80

# Start Nginx when the container starts
CMD ["nginx", "-g", "daemon off;"]