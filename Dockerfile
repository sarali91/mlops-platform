# Use an official lightweight Python base image
FROM python:3.10-slim

# Install system dependencies (Java is strictly required for PySpark)
RUN apt-get update && apt-get install -y \
    default-jre-headless \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 🔐 Hardened Security: Create a non-root user with UID 1000
RUN useradd -m -u 1000 pipelineuser

# Set up the working directory inside the container
WORKDIR /workspace

# Copy requirements and install them securely
COPY --chown=pipelineuser:pipelineuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the remaining platform source code with explicit ownership
COPY --chown=pipelineuser:pipelineuser . .

# 🔐 Hardened Security: Switch from root to the restricted user
USER 1000

# Execute the pipeline using the absolute module path
CMD ["python", "-m", "src.data_pipeline"]