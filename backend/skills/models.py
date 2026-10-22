from django.db import models
from django.conf import settings


class Skill(models.Model):
    """A skill from the shared, curated catalogue."""

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class UserSkill(models.Model):
    """A skill a user offers to teach or wants to learn."""

    class Direction(models.TextChoices):
        TEACH = "teach", "Teach"
        LEARN = "learn", "Learn"

    class Level(models.TextChoices):
        BEGINNER = "beginner", "Beginner"
        INTERMEDIATE = "intermediate", "Intermediate"
        ADVANCED = "advanced", "Advanced"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_skills")
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="user_skills")
    direction = models.CharField(max_length=5, choices=Direction.choices)
    level = models.CharField(max_length=12, choices=Level.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "skill", "direction"], name="unique_user_skill_direction")
        ]
        ordering = ["direction", "skill__name"]

    def __str__(self):
        return f"{self.user} — {self.get_direction_display()}: {self.skill}"
