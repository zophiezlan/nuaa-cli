# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set metadata
LABEL maintainer="NUAA Project"
LABEL description="NUAA CLI - AI-Assisted Project Management for NSW Users and AIDS Association"
LABEL version="0.3.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 nuaa && \
    mkdir -p /home/nuaa/.nuaa-cli /workspace && \
    chown -R nuaa:nuaa /home/nuaa /workspace

# Set working directory
WORKDIR /workspace

# Copy project files
COPY --chown=nuaa:nuaa pyproject.toml README.md ./
COPY --chown=nuaa:nuaa src/ ./src/
COPY --chown=nuaa:nuaa nuaa-kit/ ./nuaa-kit/

# Switch to non-root user
USER nuaa

# Install Python dependencies and the package
RUN pip install --user --no-cache-dir -e .

# Add user bin to PATH
ENV PATH="/home/nuaa/.local/bin:${PATH}"

# Set up volumes for persistence
VOLUME ["/workspace", "/home/nuaa/.nuaa-cli"]

# Default command
ENTRYPOINT ["nuaa"]
CMD ["--help"]
