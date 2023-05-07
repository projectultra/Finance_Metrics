# Use a base image suitable for your application
FROM python:3.8.10

# Set the working directory inside the container
WORKDIR /workspaces/Finance_Metrics/FinanceMetrics1
COPY requirements.txt .

RUN /bin/bash -c pip install -r requirements.txt
# Copy the application files to the working directory
COPY . /workspaces/Finance_Metrics/FinanceMetrics1

# Specify the command to run your application
EXPOSE 8000

# Specify the command to start your application using Gunicorn
CMD [ "python", "manage.py","runserver" ]
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "FM.wsgi:application"]
