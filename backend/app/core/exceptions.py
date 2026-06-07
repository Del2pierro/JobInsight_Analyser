from fastapi import Request
from fastapi.responses import JSONResponse


# ---------------------------------------------------------------------------
# Domain Exception Hierarchy (DDD)
# ---------------------------------------------------------------------------

class JobInsightException(Exception):
    """Base exception for all JobInsight AI business logic errors."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundException(JobInsightException):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str, identifier: str | int):
        super().__init__(
            message=f"{resource} with id '{identifier}' not found.",
            status_code=404,
        )


class ConflictException(JobInsightException):
    """Raised when a resource already exists (e.g., duplicate email)."""

    def __init__(self, resource: str, field: str, value: str):
        super().__init__(
            message=f"{resource} with {field} '{value}' already exists.",
            status_code=409,
        )


class UnauthorizedException(JobInsightException):
    """Raised when authentication fails or token is invalid."""

    def __init__(self, detail: str = "Invalid or expired credentials."):
        super().__init__(message=detail, status_code=401)


class ForbiddenException(JobInsightException):
    """Raised when the authenticated user lacks the required role/permission."""

    def __init__(self, detail: str = "You do not have permission to perform this action."):
        super().__init__(message=detail, status_code=403)


class ValidationException(JobInsightException):
    """Raised when business-level validation fails (beyond Pydantic schema)."""

    def __init__(self, detail: str):
        super().__init__(message=detail, status_code=422)


class AgentException(JobInsightException):
    """Raised when an AI agent encounters an unrecoverable error."""

    def __init__(self, agent_name: str, detail: str):
        super().__init__(
            message=f"Agent '{agent_name}' failed: {detail}",
            status_code=500,
        )


# ---------------------------------------------------------------------------
# FastAPI Global Exception Handlers
# ---------------------------------------------------------------------------

async def jobinsight_exception_handler(
    request: Request, exc: JobInsightException
) -> JSONResponse:
    """Convert any JobInsightException into a structured JSON error response."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "path": str(request.url),
        },
    )


async def generic_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Catch-all handler for unexpected errors. Never exposes raw tracebacks."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred. Please try again later.",
            "path": str(request.url),
        },
    )
