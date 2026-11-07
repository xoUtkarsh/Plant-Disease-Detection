# ==============================================================================
# Multi-stage Production Dockerfile for PhytoAI Plant Disease Detection
# ==============================================================================

FROM python:3.10-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final Runtime Image
FROM python:3.10-slim AS runner

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Copy project code
COPY src/ ./src/
COPY app/ ./app/
COPY configs/ ./configs/
COPY scripts/ ./scripts/
COPY models/ ./models/

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    mkdir -p data/sample_images data/raw data/processed && \
    chown -R appuser:appuser /app

USER appuser

# Generate sample demo leaves
RUN python scripts/create_sample_leaves.py

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
