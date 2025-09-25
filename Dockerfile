# Use official Python 3.12 slim base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY app.py .
COPY setup_data.py .
COPY streamlit_app.py .
COPY courses.csv .

# Create entrypoint script to run setup_data.py and start FastAPI
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Expose port 8000 for FastAPI
EXPOSE 8000

# Use entrypoint script to initialize and start server
CMD ["./entrypoint.sh"]