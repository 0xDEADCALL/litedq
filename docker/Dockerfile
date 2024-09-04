FROM python:3.9-slim AS base

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1

# Set workdir 
WORKDIR /app

# Copy dashboard contents
ADD dashboard . 

# Copy requirements
COPY requirements.txt requirements.txt

# Install requirements
RUN pip install -r requirements.txt

# Expose ports
EXPOSE 80

# Run streamlit dashboard
ENTRYPOINT ["streamlit", "run", "main.py" ,"--server.port=80", "--server.address=0.0.0.0"]

