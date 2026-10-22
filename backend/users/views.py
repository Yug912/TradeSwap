from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from skills.models import Skill, UserSkill
from .serializers import LoginSerializer, ProfileSerializer, RegistrationSerializer, UserSkillSerializer


def token_payload(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response({"user": ProfileSerializer(user).data, "tokens": token_payload(user)}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data["user"]
    return Response({"user": ProfileSerializer(user).data, "tokens": token_payload(user)})


@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def profile(request):
    if request.method == "GET":
        return Response(ProfileSerializer(request.user).data)
    serializer = ProfileSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(ProfileSerializer(request.user).data)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def user_skills(request):
    if request.method == "GET":
        queryset = request.user.user_skills.select_related("skill")
        return Response(UserSkillSerializer(queryset, many=True).data)
    serializer = UserSkillSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    return Response(serializer.save() and serializer.data, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def user_skill_detail(request, user_skill_id):
    deleted, _ = UserSkill.objects.filter(id=user_skill_id, user=request.user).delete()
    if not deleted:
        return Response({"detail": "Skill not found."}, status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([AllowAny])
def skills(request):
    return Response([{"id": skill.id, "name": skill.name} for skill in Skill.objects.all()])
