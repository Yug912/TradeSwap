from app.data.dummy_users import DUMMY_USERS
from app.schemas import MatchRequest, MatchResult, SkillData, UserProfile


_LEVEL_RANK = {"beginner": 1, "intermediate": 2, "advanced": 3}


def _skill_levels(skills: list[SkillData]) -> dict[str, int]:
    """Map each case-insensitive skill name to its highest listed level."""
    levels: dict[str, int] = {}
    for skill in skills:
        name = skill.skill.casefold()
        levels[name] = max(levels.get(name, 0), _LEVEL_RANK[skill.level])
    return levels


def _has_compatible_overlap(
    requested_levels: dict[str, int],
    offered_levels: dict[str, int],
) -> bool:
    """Check whether an offered skill meets at least one requested level."""
    return any(
        offered_levels.get(name, 0) >= requested_level
        for name, requested_level in requested_levels.items()
    )


def find_matches(
    user: UserProfile,
    all_users: list[UserProfile],
) -> list[MatchResult]:
    """Return profiles with reciprocal skill and proficiency compatibility."""
    if not user.teach or not user.learn:
        return []

    user_teaches = _skill_levels(user.teach)
    user_wants_to_learn = _skill_levels(user.learn)

    matches: list[MatchResult] = []
    matched_user_ids: set[int] = set()

    for candidate in all_users:
        if candidate.user_id == user.user_id or candidate.user_id in matched_user_ids:
            continue
        if not candidate.teach or not candidate.learn:
            continue

        candidate_teaches = _skill_levels(candidate.teach)
        candidate_wants_to_learn = _skill_levels(candidate.learn)

        user_can_help = _has_compatible_overlap(
            user_wants_to_learn,
            candidate_teaches,
        )
        candidate_can_help = _has_compatible_overlap(
            candidate_wants_to_learn,
            user_teaches,
        )

        if user_can_help and candidate_can_help:
            matches.append(MatchResult(user_id=candidate.user_id, score=100))
            matched_user_ids.add(candidate.user_id)

    return matches


def match_users(request: MatchRequest) -> list[MatchResult]:
    """Adapt the existing API request to matching against the Day 2 seed data."""
    return find_matches(request, DUMMY_USERS)
