from fastapi import APIRouter

from app.schemas import MatchRequest, MatchResponse
from app.services.matching import match_users


router = APIRouter(tags=["matching"])


@router.post(
    "/match",
    response_model=MatchResponse,
    summary="Find reciprocal skill matches",
    description=(
        "Find users in the local dummy dataset whose teach and learn skills "
        "match reciprocally with the submitted profile. Invalid request data "
        "is rejected with HTTP 422."
    ),
    response_description="Matching user IDs and their current match scores.",
)
def create_matches(request: MatchRequest) -> MatchResponse:
    """Validate a user profile and return its reciprocal matches."""
    return MatchResponse(matches=match_users(request))
