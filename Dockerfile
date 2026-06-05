FROM python:3.10-slim

# Install Java (Required for PySpark to run on the JVM)
RUN apt-get update && \
    apt-get install -y default-jre && \
    apt-get clean;

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code into the container
COPY src/ ./src/

# Default command to run your pipeline
CMD ["python", "src/data_pipeline.py"]