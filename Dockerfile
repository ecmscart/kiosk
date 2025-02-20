# Use the official Python image as a base
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy project files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for the port
ENV PORT=8080

# Expose the port Django will run on
EXPOSE 8080

# Run Django with Gunicorn
CMD gunicorn --bind 0.0.0.0:8080 kiosk.wsgi:application
