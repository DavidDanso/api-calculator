# Start with a Python base image (like choosing a foundation for your house)
FROM python:3.12-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file first (this helps with faster rebuilds)
COPY requirements.txt .

# Upgrade pip version
RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

# Copy your application code
COPY . .

# Expose port 8081 (like opening a window for visitors)
EXPOSE 8081

# Command to run when container starts
CMD ["python3", "app.py"]