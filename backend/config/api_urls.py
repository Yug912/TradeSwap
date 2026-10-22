from django.http import JsonResponse
from django.urls import path
from users import views as user_views


def health_check(request):
    """Minimal endpoint for confirming that the backend is available."""
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("health/", health_check, name="health-check"),
    path("register/", user_views.register, name="register"),
    path("login/", user_views.login, name="login"),
    path("profile/", user_views.profile, name="profile"),
    path("user-skills/", user_views.user_skills, name="user-skills"),
    path("user-skills/<int:user_skill_id>/", user_views.user_skill_detail, name="user-skill-detail"),
    path("skills/", user_views.skills, name="skills"),
]
