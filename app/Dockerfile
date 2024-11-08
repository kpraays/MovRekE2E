# Pull alpine library of Python for better resource utilization
FROM python:3.9.18-alpine3.18

ARG PORT
ENV PORT=${PORT}

# Install dependencies for our service
RUN apk update && apk add python3-dev \
                          gcc \
                          libc-dev 
# Set working directory as app
WORKDIR /app

# Install required libraries
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the files from our application
ADD app.py app.py
ADD container_db_connect.py container_db_connect.py 
COPY model model/
COPY data data/
COPY auto_deployment auto_deployment/

# Expose port  from the container
EXPOSE ${PORT}

# Start the Python application
CMD gunicorn --bind 0.0.0.0:$PORT app:app --threads 2 --timeout 180

# to run
# docker build -t inference .
# docker compose up -d
# docker exec -it inference /bin/bash
