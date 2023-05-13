# Base image
FROM python:3.8

# Set environment variables
ARG API_KEY
ARG NINJAAPI_KEY
ARG TWELVEDATAAPI_KEY

ENV API_KEY=$API_KEY
ENV NINJAAPI_KEY=$NINJAAPI_KEY
ENV TWELVEDATAAPI_KEY=$TWELVEDATAAPI_KEY
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the project files to the working directory
COPY . /app/

# Install dependencies
RUN pip install -r requirements.txt

# Install gunicorn
RUN pip install gunicorn

# Expose the port on which the Django app will run
EXPOSE 8000

# Set the startup command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "FM.wsgi:application"]
