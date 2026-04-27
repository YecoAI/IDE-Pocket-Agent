# --- Build Stage ---
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies in a virtualenv or just globally in this stage
COPY Backend/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt


# --- Final Stage ---
FROM python:3.11-slim

WORKDIR /app

# Create a non-root user
RUN groupadd -r idepocket && useradd -r -g idepocket idepocket

# Copy installed packages from builder
COPY --from=builder /root/.local /home/idepocket/.local
ENV PATH=/home/idepocket/.local/bin:$PATH

# Copy application code
COPY Backend/ /app/
COPY shared/ /shared/

# Create logs directory and set permissions
RUN mkdir -p /app/logs && chown -R idepocket:idepocket /app /shared

# Switch to non-root user
USER idepocket

# Expose port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
