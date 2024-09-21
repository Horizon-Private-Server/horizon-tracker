# Use official Python image from Docker Hub
FROM python:3.12

# Set the working directory in the container
WORKDIR /

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the FastAPI app
COPY . .

# Command to run the FastAPI app
CMD ["fastapi", "dev", "app/main.py", "0.0.0.0", "--port", "8000"]
  