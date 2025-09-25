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
COPY .env .

# Run setup_data.py to populate Weaviate
RUN python setup_data.py

# Expose port 8000 for FastAPI
EXPOSE 8000

# Command to run FastAPI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]