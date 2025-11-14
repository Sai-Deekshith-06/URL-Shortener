# Start from a lightweight and official Python image [3]
FROM python:3.11-slim

# Set the working directory inside the container to /app [3]
WORKDIR /code

# Copy the dependencies file first to leverage Docker's build cache
# This layer is only rebuilt if requirements.txt changes [3]
COPY requirements.txt .

# Install the Python packages listed in requirements.txt [3]
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code from the local 'app' directory into the container's working directory [3]
COPY ./app ./app

ENV PYTHONPATH="/code"

# The command to run the application when the container starts.
# This uses Gunicorn as a process manager with Uvicorn workers, which is the
# production-standard way to run a FastAPI application [5].
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000"]