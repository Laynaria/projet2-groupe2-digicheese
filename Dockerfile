# Use the official Python image
FROM python:3.11

# Set the working directory
WORKDIR /code

# Copy and install dependencies to the container
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Expose port 80 (Container HTTP)
EXPOSE 80

# Start the application
# 0.0.0.0 -> allows listening on all network interfaces (so it is accessible externally)
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80", "--reload", "--reload-dir", "api"]
# '--reload-dir' allows more efficient monitoring of changes in the 'api' directory for faster updates