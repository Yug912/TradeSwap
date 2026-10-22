"""Fictional user profiles for developing the matching service."""

from app.schemas import UserProfile


DUMMY_USERS: list[UserProfile] = [
    UserProfile(
        user_id=1,
        teach=[
            {"skill": "Python", "level": "advanced"},
            {"skill": "SQL", "level": "intermediate"},
        ],
        learn=[{"skill": "Machine Learning", "level": "beginner"}],
    ),
    UserProfile(
        user_id=2,
        teach=[{"skill": "Machine Learning", "level": "advanced"}],
        learn=[{"skill": "Python", "level": "intermediate"}],
    ),
    UserProfile(
        user_id=3,
        teach=[{"skill": "Guitar", "level": "intermediate"}],
        learn=[{"skill": "Spanish", "level": "beginner"}],
    ),
    UserProfile(
        user_id=4,
        teach=[{"skill": "Spanish", "level": "advanced"}],
        learn=[{"skill": "Guitar", "level": "beginner"}],
    ),
    UserProfile(
        user_id=5,
        teach=[{"skill": "React", "level": "intermediate"}],
        learn=[{"skill": "UI Design", "level": "beginner"}],
    ),
    UserProfile(
        user_id=6,
        teach=[{"skill": "UI Design", "level": "advanced"}],
        learn=[{"skill": "React", "level": "intermediate"}],
    ),
    UserProfile(
        user_id=7,
        teach=[{"skill": "Photography", "level": "advanced"}],
        learn=[{"skill": "Video Editing", "level": "beginner"}],
    ),
    UserProfile(
        user_id=8,
        teach=[{"skill": "Video Editing", "level": "intermediate"}],
        learn=[{"skill": "Photography", "level": "beginner"}],
    ),
]
