from django.http import JsonResponse
from django.urls import path


def health_check(request):
    """Minimal endpoint for confirming that the backend is available."""
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("health/", health_check, name="health-check"),
]
