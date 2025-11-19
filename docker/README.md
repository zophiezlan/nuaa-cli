# Docker Support

This directory provides Docker support for running NUAA CLI in containerized environments.

## Quick Start

### Using Docker Directly

```bash
# Build the image
docker build -t nuaa-cli .

# Run NUAA CLI
docker run -it --rm nuaa-cli --help

# Initialize a new project in current directory
docker run -it --rm -v $(pwd):/workspace nuaa-cli init my-project

# Run with environment variables
docker run -it --rm \
  -e LANGUAGE=en_AU \
  -e GH_TOKEN=your_github_token \
  -v $(pwd):/workspace \
  nuaa-cli init my-project
```

### Using Docker Compose

```bash
# Build and run
docker-compose up -d nuaa-cli

# Run commands
docker-compose exec nuaa-cli nuaa design "Program Name" "Population" "12 months"

# Development environment with all tools
docker-compose run --rm nuaa-dev

# Run tests in container
docker-compose run --rm nuaa-dev pytest

# Stop containers
docker-compose down
```

## Available Images

### Production Image (`Dockerfile`)
- **Base**: `python:3.11-slim`
- **Size**: ~200MB
- **Purpose**: Running NUAA CLI commands
- **Includes**: Git, NUAA CLI package
- **User**: Non-root user `nuaa`

### Development Image (`Dockerfile.dev`)
- **Base**: `python:3.11-slim`
- **Size**: ~350MB
- **Purpose**: Development and testing
- **Includes**: Git, Make, development tools, test dependencies
- **User**: Non-root user `nuaa`

## Environment Variables

Configure NUAA CLI behavior:

```bash
# Language/Locale
-e LANGUAGE=en_AU           # en_AU, vi_VN, th_TH, ar, zh_CN, es

# GitHub Authentication
-e GH_TOKEN=ghp_xxx         # GitHub personal access token
-e GITHUB_TOKEN=ghp_xxx     # Alternative token variable

# Accessibility
-e NUAA_ACCESSIBILITY_MODE=standard  # standard, screen-reader, high-contrast, etc.
-e NO_COLOR=1               # Disable colors

# Logging
-e LOG_LEVEL=INFO           # DEBUG, INFO, WARNING, ERROR
-e DEBUG=1                  # Enable debug mode
```

## Volume Mounts

### Workspace Directory
Mount your project directory to `/workspace`:

```bash
docker run -it --rm -v $(pwd):/workspace nuaa-cli init my-project
```

### Configuration Directory
Persist NUAA CLI configuration:

```bash
docker run -it --rm \
  -v $(pwd):/workspace \
  -v nuaa-config:/home/nuaa/.nuaa-cli \
  nuaa-cli init my-project
```

## Examples

### Initialize a New Project

```bash
docker run -it --rm -v $(pwd):/workspace nuaa-cli \
  init my-project --ai-assistant claude --script-type sh
```

### Create Program Design

```bash
docker run -it --rm -v $(pwd)/my-project:/workspace nuaa-cli \
  design "Peer Support Program" "PWUD in Sydney" "12 months"
```

### Create Proposal

```bash
docker run -it --rm -v $(pwd)/my-project:/workspace nuaa-cli \
  propose "Peer Support Program" "NSW Health" "$50000" "12 months"
```

### Run Tests (Development)

```bash
# Run all tests
docker-compose run --rm nuaa-dev pytest

# Run specific test file
docker-compose run --rm nuaa-dev pytest tests/test_cli_basic.py

# Run with coverage
docker-compose run --rm nuaa-dev pytest --cov=src/nuaa_cli --cov-report=html
```

### Development Workflow

```bash
# Start development environment
docker-compose run --rm nuaa-dev

# Inside container:
nuaa@container:/workspace$ pytest
nuaa@container:/workspace$ make lint
nuaa@container:/workspace$ make format
nuaa@container:/workspace$ nuaa init test-project
```

## Building Custom Images

### With Custom Base Image

```dockerfile
FROM python:3.12-slim
# ... rest of Dockerfile
```

### With Additional Tools

```dockerfile
# Add to Dockerfile
RUN apt-get update && apt-get install -y \
    vim \
    tmux \
    && rm -rf /var/lib/apt/lists/*
```

### Multi-stage Build (Smaller Image)

```dockerfile
# Build stage
FROM python:3.11 AS builder
WORKDIR /app
COPY pyproject.toml .
COPY src/ ./src/
RUN pip install --user --no-cache-dir -e .

# Runtime stage
FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
ENTRYPOINT ["nuaa"]
```

## Troubleshooting

### Permission Issues

If you encounter permission issues:

```bash
# Run as current user
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v $(pwd):/workspace \
  nuaa-cli init my-project
```

### Git Configuration

Configure git inside container:

```bash
docker run -it --rm \
  -e GIT_AUTHOR_NAME="Your Name" \
  -e GIT_AUTHOR_EMAIL="you@example.com" \
  -e GIT_COMMITTER_NAME="Your Name" \
  -e GIT_COMMITTER_EMAIL="you@example.com" \
  -v $(pwd):/workspace \
  nuaa-cli init my-project
```

### Network Issues

If experiencing network issues:

```bash
# Use host network
docker run -it --rm --network host -v $(pwd):/workspace nuaa-cli init my-project

# Set DNS
docker run -it --rm --dns 8.8.8.8 -v $(pwd):/workspace nuaa-cli init my-project
```

## CI/CD Integration

### GitHub Actions

```yaml
name: NUAA CLI
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker build -t nuaa-cli:test -f Dockerfile.dev .
      - name: Run tests
        run: docker run nuaa-cli:test pytest
```

### GitLab CI

```yaml
test:
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t nuaa-cli:test -f Dockerfile.dev .
    - docker run nuaa-cli:test pytest
```

## Security Considerations

- ✅ **Non-root user**: Container runs as `nuaa` user (UID 1000)
- ✅ **Minimal base image**: Uses `python:3.11-slim` to reduce attack surface
- ✅ **No cache**: Development dependencies not cached in production image
- ✅ **Volume isolation**: Configuration stored in named volumes
- ✅ **Read-only root**: Can be enforced with `--read-only` flag

## Performance

Typical startup times:
- **Cold start**: ~2-3 seconds
- **Warm start**: ~0.5 seconds
- **Command execution**: Varies by command

Image sizes:
- **Production**: ~200MB
- **Development**: ~350MB

## Publishing Images

### To Docker Hub

```bash
# Tag image
docker tag nuaa-cli:latest yourusername/nuaa-cli:latest
docker tag nuaa-cli:latest yourusername/nuaa-cli:0.3.0

# Push image
docker push yourusername/nuaa-cli:latest
docker push yourusername/nuaa-cli:0.3.0
```

### To GitHub Container Registry

```bash
# Tag for GHCR
docker tag nuaa-cli:latest ghcr.io/zophiezlan/nuaa-cli:latest

# Login and push
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
docker push ghcr.io/zophiezlan/nuaa-cli:latest
```
