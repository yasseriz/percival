FROM python:3.11.9-slim

# Set Environment Variables
ENV PYTHONUNBUFFERED 1
ENV APP_HOME /fastapi

# Set working directory
WORKDIR $APP_HOME

# Copy requirements and install dependencies
COPY docker/fastapi/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./app /${APP_HOME}/app/

# Expose the port for FASTApi
EXPOSE 8000

# Run the FastAPI server using Uvivorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]