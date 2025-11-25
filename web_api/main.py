"""
NUAA CLI Web API Backend

This module provides a FastAPI-based web backend for the NUAA CLI,
enabling web-based access to NUAA CLI functionality.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Security, Depends
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uuid
import os
import secrets

# Import NUAA CLI functions
from nuaa_cli.scaffold import (
    _ensure_nuaa_root,
    _next_feature_dir,
    _load_template,
    _apply_replacements,
    _prepend_metadata,
    _write_markdown,
)
from nuaa_cli.utils import validate_program_name, validate_text_field
from rich.console import Console

app = FastAPI(
    title="NUAA CLI API",
    description="Web API for NUAA Project Kit - AI-Assisted Project Management",
    version="0.3.0",
)

# Configure CORS with environment-based origins
# Default to localhost only for security. Set NUAA_API_ALLOWED_ORIGINS for production.
# Example: NUAA_API_ALLOWED_ORIGINS="https://app.example.com,https://app2.example.com"
allowed_origins_env = os.getenv("NUAA_API_ALLOWED_ORIGINS", "")
if allowed_origins_env:
    # Production: use specified origins from environment
    allowed_origins = [origin.strip() for origin in allowed_origins_env.split(",")]
elif os.getenv("NUAA_API_DEV_MODE", "").lower() in ("true", "1", "yes"):
    # Development mode: allow all origins (explicitly opt-in only)
    allowed_origins = ["*"]
else:
    # Default: localhost only for security
    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# API Key Authentication
# Set NUAA_API_KEY environment variable to enable authentication
# If not set, API runs in open mode (suitable for local development only)
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)
CONFIGURED_API_KEY = os.getenv("NUAA_API_KEY", "")


async def verify_api_key(api_key: str = Security(API_KEY_HEADER)):
    """
    Verify API key from request header.

    If NUAA_API_KEY is not set, allows all requests (development mode).
    In production, set NUAA_API_KEY to require authentication.
    """
    if not CONFIGURED_API_KEY:
        # No API key configured - allow all requests (development mode)
        return None

    if api_key is None:
        raise HTTPException(
            status_code=401,
            detail="API key required. Include 'X-API-Key' header with your request.",
        )

    # Constant-time comparison to prevent timing attacks
    if not secrets.compare_digest(api_key, CONFIGURED_API_KEY):
        raise HTTPException(status_code=403, detail="Invalid API key")

    return api_key


# Global state (use database in production)
projects: Dict[str, Dict[str, Any]] = {}
console = Console()


# Pydantic models for request/response
class HealthResponse(BaseModel):
    status: str
    version: str


class ProgramDesignRequest(BaseModel):
    program_name: str = Field(..., description="Name of the program")
    target_population: str = Field(..., description="Target population description")
    duration: str = Field(..., description="Program duration (e.g., '6 months')")
    feature: Optional[str] = Field(None, description="Custom feature slug")
    force: bool = Field(False, description="Overwrite existing files")


class ProposalRequest(BaseModel):
    program_name: str
    funder: str
    amount: str
    duration: str
    force: bool = False


class MeasureRequest(BaseModel):
    program_name: str
    evaluation_period: str
    budget: str
    force: bool = False


class ProjectResponse(BaseModel):
    id: str
    status: str
    message: str
    files_created: List[str] = []


# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy", version="0.3.0")


# Design endpoint
@app.post("/api/design", response_model=ProjectResponse)
async def create_program_design(
    request: ProgramDesignRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key),
):
    """
    Create a new NUAA program design with logic model.

    This endpoint creates:
    - program-design.md
    - logic-model.md
    - impact-framework.md
    """
    try:
        # Validate inputs
        program_name = validate_program_name(request.program_name, console)
        target_population = validate_text_field(
            request.target_population, "target_population", 500, console
        )
        duration = validate_text_field(request.duration, "duration", 100, console)

        # Generate project ID
        project_id = str(uuid.uuid4())

        # Determine feature directory
        if request.feature:
            feature_dir = _ensure_nuaa_root() / request.feature
            feature_dir.mkdir(parents=True, exist_ok=True)
            slug = request.feature
        else:
            feature_dir, num_str, slug = _next_feature_dir(program_name)

        # Create design files
        from datetime import datetime

        created = datetime.now().strftime("%Y-%m-%d")

        mapping = {
            "PROGRAM_NAME": program_name,
            "TARGET_POPULATION": target_population,
            "DURATION": duration,
            "DATE": created,
        }

        files_created = []

        # Create program-design.md
        template = _load_template("program-design.md")
        filled = _apply_replacements(template, mapping)
        meta = {
            "title": f"{program_name} - Program Design",
            "created": created,
            "status": "draft",
        }
        text = _prepend_metadata(filled, meta)
        dest = feature_dir / "program-design.md"

        # Check if file exists and force flag
        if dest.exists() and not request.force:
            raise HTTPException(
                status_code=409,
                detail=f"Program design already exists at {dest}. Use force=true to overwrite.",
            )

        _write_markdown(dest, text)
        files_created.append(str(dest))

        # Store project info
        projects[project_id] = {
            "id": project_id,
            "program_name": program_name,
            "feature_dir": str(feature_dir),
            "files_created": files_created,
        }

        return ProjectResponse(
            id=project_id,
            status="success",
            message=f"Program design created for '{program_name}'",
            files_created=files_created,
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Propose endpoint
@app.post("/api/propose", response_model=ProjectResponse)
async def create_proposal(request: ProposalRequest, api_key: str = Depends(verify_api_key)):
    """
    Create a funding proposal for an existing program.
    """
    try:
        program_name = validate_program_name(request.program_name, console)
        funder = validate_text_field(request.funder, "funder", 200, console)
        amount = validate_text_field(request.amount, "amount", 50, console)
        duration = validate_text_field(request.duration, "duration", 100, console)

        project_id = str(uuid.uuid4())

        # Find or create feature directory for the program
        from nuaa_cli.scaffold import get_or_create_feature_dir

        feature_dir = get_or_create_feature_dir(program_name)

        # Create proposal file
        from datetime import datetime

        created = datetime.now().strftime("%Y-%m-%d")

        mapping = {
            "PROGRAM_NAME": program_name,
            "FUNDER": funder,
            "AMOUNT": amount,
            "DURATION": duration,
            "DATE": created,
        }

        files_created = []

        # Create proposal.md
        template = _load_template("proposal.md")
        filled = _apply_replacements(template, mapping)
        meta = {
            "title": f"{program_name} - Funding Proposal",
            "funder": funder,
            "created": created,
            "status": "draft",
        }
        text = _prepend_metadata(filled, meta)
        dest = feature_dir / "proposal.md"

        # Check if file exists and force flag
        if dest.exists() and not request.force:
            raise HTTPException(
                status_code=409,
                detail=f"Proposal already exists at {dest}. Use force=true to overwrite.",
            )

        _write_markdown(dest, text)
        files_created.append(str(dest))

        # Store project info
        projects[project_id] = {
            "id": project_id,
            "program_name": program_name,
            "feature_dir": str(feature_dir),
            "files_created": files_created,
        }

        return ProjectResponse(
            id=project_id,
            status="success",
            message=f"Proposal created for '{program_name}'",
            files_created=files_created,
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Measure endpoint
@app.post("/api/measure", response_model=ProjectResponse)
async def create_impact_framework(request: MeasureRequest, api_key: str = Depends(verify_api_key)):
    """
    Create an impact measurement framework.
    """
    try:
        program_name = validate_program_name(request.program_name, console)
        evaluation_period = validate_text_field(
            request.evaluation_period, "evaluation_period", 100, console
        )
        budget = validate_text_field(request.budget, "budget", 100, console)

        project_id = str(uuid.uuid4())

        # Find or create feature directory for the program
        from nuaa_cli.scaffold import get_or_create_feature_dir

        feature_dir = get_or_create_feature_dir(program_name)

        # Create measurement framework file
        from datetime import datetime

        created = datetime.now().strftime("%Y-%m-%d")

        mapping = {
            "PROGRAM_NAME": program_name,
            "EVALUATION_PERIOD": evaluation_period,
            "BUDGET": budget,
            "DATE": created,
        }

        files_created = []

        # Create measurement-framework.md
        template = _load_template("measurement-framework.md")
        filled = _apply_replacements(template, mapping)
        meta = {
            "title": f"{program_name} - Impact Measurement Framework",
            "evaluation_period": evaluation_period,
            "created": created,
            "status": "draft",
        }
        text = _prepend_metadata(filled, meta)
        dest = feature_dir / "measurement-framework.md"

        # Check if file exists and force flag
        if dest.exists() and not request.force:
            raise HTTPException(
                status_code=409,
                detail=f"Measurement framework already exists at {dest}. Use force=true to overwrite.",
            )

        _write_markdown(dest, text)
        files_created.append(str(dest))

        # Store project info
        projects[project_id] = {
            "id": project_id,
            "program_name": program_name,
            "feature_dir": str(feature_dir),
            "files_created": files_created,
        }

        return ProjectResponse(
            id=project_id,
            status="success",
            message=f"Impact framework created for '{program_name}'",
            files_created=files_created,
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# List projects endpoint
@app.get("/api/projects")
async def list_projects(api_key: str = Depends(verify_api_key)):
    """
    List all projects created via the API.

    Requires authentication if NUAA_API_KEY is set.
    """
    return {"projects": list(projects.values())}


# Get project endpoint
@app.get("/api/projects/{project_id}")
async def get_project(project_id: str, api_key: str = Depends(verify_api_key)):
    """
    Get details of a specific project.

    Requires authentication if NUAA_API_KEY is set.
    """
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")

    return projects[project_id]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
