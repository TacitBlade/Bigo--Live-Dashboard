#!/bin/bash
# Simple startup script for the Streamlit application

echo "Starting Streamlit application..."

# Set environment variables
export PYTHONPATH="/app:$PYTHONPATH"
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_ENABLE_CORS=false

# Start the application
streamlit run home.py \
    --server.port=${PORT:-8501} \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false
