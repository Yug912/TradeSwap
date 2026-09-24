from app.schemas import MatchRequest, MatchResult


def match_users(request: MatchRequest) -> list[MatchResult]:
    """Return placeholder results until weighted matching is implemented."""
    # TODO: add weighted skill, level, and availability matching.
    del request
    return []