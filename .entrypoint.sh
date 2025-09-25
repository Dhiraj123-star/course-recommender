#!/bin/bash
# Run setup_data.py to populate Weaviate
python setup_data.py
# Start FastAPI server
exec uvicorn app:app --host 0.0.0.0 --port 8000