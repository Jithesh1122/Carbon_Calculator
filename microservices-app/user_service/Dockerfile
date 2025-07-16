# Use an official Python runtime as a base
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy application files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5001

# Run the application
CMD ["python", "app.py"]
