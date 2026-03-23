# =============================================================================
#  Dockerfile - Container for the Greeter API
# =============================================================================
#
#  In a real CI/CD pipeline, the BUILD stage creates this Docker image
#  and the DEPLOY stage pushes it to a registry and deploys it.
#
#  Build:  docker build -t greeter-api .
#  Run:    docker run -p 5000:5000 greeter-api
#  Test:   curl http://localhost:5000/health
#
# =============================================================================

FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy dependency file first (for Docker layer caching)
# This means if only app code changes, pip install is cached!
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Expose the Flask port
EXPOSE 5000

# Health check (Docker will monitor this)
# If /health stops responding, Docker marks the container as unhealthy
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health')" || exit 1

# Run the API
CMD ["python", "-m", "app.api"]
