# NUAA CLI Web API

This directory contains a FastAPI-based web backend for the NUAA CLI.

## Features

- RESTful API for NUAA CLI commands
- Interactive API documentation (Swagger UI)
- CORS support for web clients
- Input validation with Pydantic
- Background task processing

## Installation

```bash
# Install FastAPI and dependencies
pip install fastapi uvicorn[standard] pydantic

# Or add to pyproject.toml
[project.optional-dependencies]
web = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "pydantic>=2.4.0",
]
```

## Running the Server

### Development

```bash
# Start development server with auto-reload
uvicorn web_api.main:app --reload

# Or use Python directly
python -m web_api.main

# Specify host and port
uvicorn web_api.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production

```bash
# Using Uvicorn with workers
uvicorn web_api.main:app --host 0.0.0.0 --port 8000 --workers 4

# Using Gunicorn with Uvicorn workers
gunicorn web_api.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

## API Endpoints

### Health Check

```bash
GET /health

Response:
{
  "status": "healthy",
  "version": "0.3.0"
}
```

### Create Program Design

```bash
POST /api/design

Body:
{
  "program_name": "Peer Support Program",
  "target_population": "PWUD in Sydney",
  "duration": "12 months",
  "feature": null,
  "force": false
}

Response:
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "success",
  "message": "Program design created for 'Peer Support Program'",
  "files_created": ["/path/to/program-design.md"]
}
```

### Create Proposal

```bash
POST /api/propose

Body:
{
  "program_name": "Peer Support Program",
  "funder": "NSW Health",
  "amount": "$50000",
  "duration": "12 months"
}
```

### Create Impact Framework

```bash
POST /api/measure

Body:
{
  "program_name": "Peer Support Program",
  "evaluation_period": "Q1 2024",
  "budget": "$5000"
}
```

### List Projects

```bash
GET /api/projects

Response:
{
  "projects": [
    {
      "id": "123e4567...",
      "program_name": "Peer Support Program",
      "feature_dir": "/path/to/nuaa/001-peer-support",
      "files_created": [...]
    }
  ]
}
```

### Get Project

```bash
GET /api/projects/{project_id}
```

## Interactive Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Example Usage

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Create program design
curl -X POST http://localhost:8000/api/design \
  -H "Content-Type: application/json" \
  -d '{
    "program_name": "Peer Support Program",
    "target_population": "PWUD in Sydney",
    "duration": "12 months"
  }'
```

### Using Python Requests

```python
import requests

# Create program design
response = requests.post(
    "http://localhost:8000/api/design",
    json={
        "program_name": "Peer Support Program",
        "target_population": "PWUD in Sydney",
        "duration": "12 months",
    }
)

project = response.json()
print(f"Created project: {project['id']}")
print(f"Files created: {project['files_created']}")
```

### Using JavaScript/Fetch

```javascript
// Create program design
const response = await fetch('http://localhost:8000/api/design', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    program_name: 'Peer Support Program',
    target_population: 'PWUD in Sydney',
    duration: '12 months',
  }),
});

const project = await response.json();
console.log('Created project:', project.id);
```

## Configuration

### Environment Variables

```bash
# Server configuration
export API_HOST=0.0.0.0
export API_PORT=8000
export API_WORKERS=4

# CORS configuration
export CORS_ORIGINS="http://localhost:3000,https://app.nuaa.org"

# Logging
export LOG_LEVEL=INFO
```

### CORS Configuration

Update `main.py` to configure allowed origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://app.nuaa.org",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

## Docker Support

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
COPY src/ ./src/
COPY web_api/ ./web_api/

RUN pip install -e ".[web]"

EXPOSE 8000

CMD ["uvicorn", "web_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Run with Docker

```bash
# Build image
docker build -t nuaa-cli-api .

# Run container
docker run -p 8000:8000 nuaa-cli-api
```

## Testing the API

```bash
# Run API tests
pytest tests/test_api.py

# Test with coverage
pytest tests/test_api.py --cov=web_api
```

## Production Deployment

### Using Systemd

Create `/etc/systemd/system/nuaa-api.service`:

```ini
[Unit]
Description=NUAA CLI API
After=network.target

[Service]
Type=notify
User=nuaa
WorkingDirectory=/opt/nuaa-cli
Environment="PATH=/opt/nuaa-cli/venv/bin"
ExecStart=/opt/nuaa-cli/venv/bin/uvicorn web_api.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable nuaa-api
sudo systemctl start nuaa-api
```

### Using Docker Compose

```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - LOG_LEVEL=INFO
    volumes:
      - ./workspace:/workspace
    restart: always
```

### Using Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name api.nuaa.org;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Security Considerations

1. **Authentication**: Add JWT or OAuth2 for production
2. **Rate Limiting**: Implement rate limiting to prevent abuse
3. **Input Validation**: All inputs are validated (already implemented)
4. **CORS**: Configure allowed origins appropriately
5. **HTTPS**: Use SSL/TLS in production (via Nginx/Caddy)

## Future Enhancements

- [ ] Add authentication (JWT/OAuth2)
- [ ] Add rate limiting
- [ ] Add database persistence (PostgreSQL/MongoDB)
- [ ] Add WebSocket support for real-time updates
- [ ] Add file upload endpoints
- [ ] Add export endpoints (PDF, ZIP)
- [ ] Add user management
- [ ] Add project sharing/collaboration

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
