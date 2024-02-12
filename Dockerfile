# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
# Note: Ensure that requirements.txt is available during build
COPY requirements.txt ./
RUN pip install --no-cache-dir --default-timeout=120 -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the app. CMD can be overridden by command line arguments passed to docker run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]