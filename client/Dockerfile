FROM python:3.12

RUN mkdir /app

WORKDIR /app
# Set environment variables
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y tshark && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY requirements.txt  /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app/
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]