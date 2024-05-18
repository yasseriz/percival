FROM python:3.11.9-slim

# SET Environment Variables
ENV PYTHONUNBUFFERED 1
ENV APP_HOME=/web_interface

# Set the working directory
WORKDIR $APP_HOME

# Copy requirements and install dependencies
COPY docker/streamlit/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Streamlit app code into the container
COPY web_interface/ .

# Expose port for Streamlit
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "web_interface/streamlit_app.py", "--server.port=8501", "--server.headless=true"]