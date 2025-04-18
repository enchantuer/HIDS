# Choose the python version
FROM python:3.12

RUN mkdir /app

WORKDIR /app
# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

RUN apt update && apt install -y libasound2-dev

# Upgrade pip
RUN pip install --upgrade pip

# Copy the Django project  and install dependencies
COPY requirements.txt  /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project to the container
COPY ./app /app/
RUN chmod +x /app/entrypoint.sh

# Expose the port for communication with HIDS
EXPOSE 4433
# Expose the port for the web interface (Django port)
EXPOSE 8000

# Run Django’s development server
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
ENTRYPOINT ["/app/entrypoint.sh"]
