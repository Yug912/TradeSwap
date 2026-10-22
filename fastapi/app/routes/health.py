from fastapi import APIRouter


router = APIRouter(tags=["health"])


@router.get(
    "/health",
    summary="Health check",
    description="Check that the TradeSwap matching API is running.",
    response_description="The service health status.",
)
def health_check() -> dict[str, str]:
    """Return a simple status payload when the API is available."""
    return {"status": "ok"}
