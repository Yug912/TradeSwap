from fastapi.testclient import TestClient
from pydantic import ValidationError
import pytest

from app.data.dummy_users import DUMMY_USERS
from app.main import app
from app.routes import match as match_route
from app.schemas import (
    MatchRequest,
    MatchResponse,
    MatchResult,
    SkillData,
    UserProfile,
)
from app.services.matching import find_matches


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_cors_allows_configured_local_frontend_origin() -> None:
    response = client.options(
        "/match",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_cors_does_not_allow_unconfigured_origin() -> None:
    response = client.options(
        "/match",
        headers={
            "Origin": "https://untrusted.example",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers


def test_unexpected_server_error_does_not_expose_internal_details(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def raise_unexpected_error(_request: MatchRequest) -> list[MatchResult]:
        raise RuntimeError("sensitive internal diagnostic")

    monkeypatch.setattr(match_route, "match_users", raise_unexpected_error)
    error_client = TestClient(app, raise_server_exceptions=False)

    response = error_client.post(
        "/match",
        json={"user_id": 1, "teach": [], "learn": []},
    )

    assert response.status_code == 500
    assert response.text == "Internal Server Error"
    assert "sensitive internal diagnostic" not in response.text
    assert "Traceback" not in response.text


def test_openapi_documents_health_and_match_schemas() -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
    schema = response.json()
    health_operation = schema["paths"]["/health"]["get"]
    match_operation = schema["paths"]["/match"]["post"]

    assert health_operation["summary"] == "Health check"
    health_response_schema = health_operation["responses"]["200"]["content"][
        "application/json"
    ]["schema"]
    assert health_response_schema["type"] == "object"
    assert health_response_schema["additionalProperties"]["type"] == "string"
    assert match_operation["summary"] == "Find reciprocal skill matches"
    assert (
        match_operation["requestBody"]["content"]["application/json"]["schema"]["$ref"]
        == "#/components/schemas/MatchRequest"
    )
    assert (
        match_operation["responses"]["200"]["content"]["application/json"]["schema"]["$ref"]
        == "#/components/schemas/MatchResponse"
    )
    assert "422" in match_operation["responses"]


def test_match_accepts_valid_request() -> None:
    response = client.post(
        "/match",
        json={
            "user_id": 1,
            "teach": [
                {"skill": "Python", "level": "advanced"},
                {"skill": "C++", "level": "intermediate"},
            ],
            "learn": [{"skill": "Machine Learning", "level": "beginner"}],
        },
    )

    assert response.status_code == 200
    assert response.json() == {"matches": [{"user_id": 2, "score": 100.0}]}
    assert MatchResponse.model_validate(response.json()).matches == [
        MatchResult(user_id=2, score=100)
    ]


def test_match_accepts_valid_request_with_no_matches() -> None:
    response = client.post(
        "/match",
        json={
            "user_id": 101,
            "teach": [{"skill": "Cooking", "level": "advanced"}],
            "learn": [{"skill": "Astronomy", "level": "beginner"}],
        },
    )

    assert response.status_code == 200
    assert MatchResponse.model_validate(response.json()) == MatchResponse(matches=[])


def test_match_rejects_invalid_request() -> None:
    response = client.post(
        "/match",
        json={"user_id": "not-an-integer", "teach": [], "learn": []},
    )

    assert response.status_code == 422


def test_match_rejects_invalid_proficiency_level_with_422() -> None:
    response = client.post(
        "/match",
        json={
            "user_id": 101,
            "teach": [{"skill": "Python", "level": "expert"}],
            "learn": [],
        },
    )

    assert response.status_code == 422


def test_skill_data_accepts_supported_proficiency_levels() -> None:
    for level in ("beginner", "intermediate", "advanced"):
        assert SkillData(skill="Python", level=level).level == level


def test_skill_data_rejects_unsupported_proficiency_level() -> None:
    with pytest.raises(ValidationError):
        SkillData(skill="Python", level="expert")


def test_user_profile_and_match_request_share_the_existing_contract() -> None:
    profile = UserProfile(
        user_id=42,
        teach=[{"skill": "Python", "level": "advanced"}],
        learn=[{"skill": "Rust", "level": "beginner"}],
    )
    request = MatchRequest.model_validate(profile.model_dump())

    assert request.user_id == profile.user_id
    assert request.teach == profile.teach
    assert request.learn == profile.learn
    assert MatchResponse(matches=[MatchResult(user_id=7, score=82.5)]).model_dump() == {
        "matches": [{"user_id": 7, "score": 82.5}]
    }


def test_dummy_users_are_valid_unique_profiles_with_teach_and_learn_skills() -> None:
    assert 5 <= len(DUMMY_USERS) <= 10
    assert all(isinstance(user, UserProfile) for user in DUMMY_USERS)
    assert len({user.user_id for user in DUMMY_USERS}) == len(DUMMY_USERS)
    assert all(user.teach and user.learn for user in DUMMY_USERS)
    assert all(
        skill.level in {"beginner", "intermediate", "advanced"}
        for user in DUMMY_USERS
        for skill in (*user.teach, *user.learn)
    )


def test_find_matches_returns_reciprocal_match_by_skill_name() -> None:
    user = UserProfile(
        user_id=101,
        teach=[{"skill": "Python", "level": "advanced"}],
        learn=[{"skill": "Guitar", "level": "beginner"}],
    )
    candidate = UserProfile(
        user_id=102,
        teach=[{"skill": "Guitar", "level": "intermediate"}],
        learn=[{"skill": "Python", "level": "beginner"}],
    )

    assert find_matches(user, [candidate]) == [MatchResult(user_id=102, score=100)]


def test_find_matches_rejects_one_way_overlap() -> None:
    user = UserProfile(
        user_id=101,
        teach=[{"skill": "Python", "level": "advanced"}],
        learn=[{"skill": "Guitar", "level": "beginner"}],
    )
    candidate = UserProfile(
        user_id=102,
        teach=[{"skill": "Guitar", "level": "intermediate"}],
        learn=[{"skill": "Spanish", "level": "beginner"}],
    )

    assert find_matches(user, [candidate]) == []


def test_find_matches_returns_empty_when_neither_direction_overlaps() -> None:
    user = UserProfile(
        user_id=101,
        teach=[{"skill": "Python", "level": "advanced"}],
        learn=[{"skill": "Guitar", "level": "beginner"}],
    )
    candidate = UserProfile(
        user_id=102,
        teach=[{"skill": "Spanish", "level": "intermediate"}],
        learn=[{"skill": "Cooking", "level": "beginner"}],
    )

    assert find_matches(user, [candidate]) == []


def test_find_matches_uses_dummy_dataset_without_duplicate_results() -> None:
    matches = find_matches(DUMMY_USERS[0], [*DUMMY_USERS, DUMMY_USERS[1]])

    assert matches == [MatchResult(user_id=2, score=100)]
    assert len({match.user_id for match in matches}) == len(matches)


def test_match_endpoint_preserves_existing_response_contract() -> None:
    response = client.post(
        "/match",
        json={
            "user_id": DUMMY_USERS[0].user_id,
            "teach": [skill.model_dump() for skill in DUMMY_USERS[0].teach],
            "learn": [skill.model_dump() for skill in DUMMY_USERS[0].learn],
        },
    )

    assert response.status_code == 200
    assert response.json() == {"matches": [{"user_id": 2, "score": 100.0}]}


def test_find_matches_excludes_self_even_with_perfect_overlap() -> None:
    user = UserProfile(
        user_id=101,
        teach=[{"skill": "Python", "level": "advanced"}],
        learn=[{"skill": "Python", "level": "advanced"}],
    )

    assert find_matches(user, [user]) == []


def test_find_matches_returns_empty_when_user_has_no_teach_skills() -> None:
    user = UserProfile(
        user_id=101,
        learn=[{"skill": "Python", "level": "beginner"}],
    )
    candidate = UserProfile(
        user_id=102,
        teach=[{"skill": "Python", "level": "advanced"}],
        learn=[{"skill": "Spanish", "level": "beginner"}],
    )

    assert find_matches(user, [candidate]) == []


def test_find_matches_returns_empty_when_user_has_no_learn_skills() -> None:
    user = UserProfile(
        user_id=101,
        teach=[{"skill": "Python", "level": "advanced"}],
    )
    candidate = UserProfile(
        user_id=102,
        teach=[{"skill": "Spanish", "level": "advanced"}],
        learn=[{"skill": "Python", "level": "beginner"}],
    )

    assert find_matches(user, [candidate]) == []


@pytest.mark.parametrize(
    "candidate",
    [
        UserProfile(
            user_id=102,
            learn=[{"skill": "Python", "level": "beginner"}],
        ),
        UserProfile(
            user_id=103,
            teach=[{"skill": "Guitar", "level": "advanced"}],
        ),
    ],
)
def test_find_matches_skips_candidates_with_an_empty_skill_list(
    candidate: UserProfile,
) -> None:
    user = UserProfile(
        user_id=101,
        teach=[{"skill": "Python", "level": "advanced"}],
        learn=[{"skill": "Guitar", "level": "beginner"}],
    )

    assert find_matches(user, [candidate]) == []


def test_find_matches_deduplicates_case_insensitive_skill_entries() -> None:
    user = UserProfile(
        user_id=101,
        teach=[
            {"skill": "Python", "level": "advanced"},
            {"skill": "PYTHON", "level": "beginner"},
        ],
        learn=[
            {"skill": "Guitar", "level": "beginner"},
            {"skill": "GUITAR", "level": "beginner"},
        ],
    )
    candidate = UserProfile(
        user_id=102,
        teach=[
            {"skill": "guitar", "level": "intermediate"},
            {"skill": "GUITAR", "level": "beginner"},
        ],
        learn=[
            {"skill": "python", "level": "beginner"},
            {"skill": "PYTHON", "level": "beginner"},
        ],
    )

    assert find_matches(user, [candidate]) == [MatchResult(user_id=102, score=100)]


def test_find_matches_deduplicates_candidate_ids() -> None:
    user = UserProfile(
        user_id=101,
        teach=[{"skill": "Python", "level": "advanced"}],
        learn=[{"skill": "Guitar", "level": "beginner"}],
    )
    first_candidate = UserProfile(
        user_id=102,
        teach=[{"skill": "Guitar", "level": "intermediate"}],
        learn=[{"skill": "Python", "level": "beginner"}],
    )
    duplicate_candidate = first_candidate.model_copy(deep=True)

    assert find_matches(user, [first_candidate, duplicate_candidate]) == [
        MatchResult(user_id=102, score=100)
    ]


def test_find_matches_accepts_sufficient_proficiency_in_both_directions() -> None:
    user = UserProfile(
        user_id=101,
        teach=[{"skill": "Python", "level": "intermediate"}],
        learn=[{"skill": "Guitar", "level": "beginner"}],
    )
    candidate = UserProfile(
        user_id=102,
        teach=[{"skill": "Guitar", "level": "intermediate"}],
        learn=[{"skill": "Python", "level": "beginner"}],
    )

    assert find_matches(user, [candidate]) == [MatchResult(user_id=102, score=100)]


def test_find_matches_rejects_insufficient_proficiency() -> None:
    user = UserProfile(
        user_id=101,
        teach=[{"skill": "Python", "level": "advanced"}],
        learn=[{"skill": "Guitar", "level": "advanced"}],
    )
    candidate = UserProfile(
        user_id=102,
        teach=[{"skill": "Guitar", "level": "intermediate"}],
        learn=[{"skill": "Python", "level": "advanced"}],
    )

    assert find_matches(user, [candidate]) == []


def test_skill_without_proficiency_level_is_rejected_by_existing_schema() -> None:
    with pytest.raises(ValidationError):
        UserProfile(
            user_id=101,
            teach=[{"skill": "Python"}],
            learn=[{"skill": "Guitar", "level": "beginner"}],
        )
