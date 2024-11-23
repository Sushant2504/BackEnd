FROM python:3.10-slim

WORKDIR /Backend

COPY requirement.txt .

RUN pip install -r requirement.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Set the command to run the FastAPI application with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
