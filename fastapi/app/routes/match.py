from fastapi import APIRouter

from app.schemas import MatchRequest, MatchResponse
from app.services.matching import match_users


router = APIRouter(tags=["matching"])


@router.post("/match", response_model=MatchResponse)
def create_matches(request: MatchRequest) -> MatchResponse:
    return MatchResponse(matches=match_users(request))