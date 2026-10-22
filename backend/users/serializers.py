from django.contrib.auth import authenticate
from rest_framework import serializers

from skills.models import Skill, UserSkill
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("username", "email", "password", "first_name", "last_name")

    def create(self, validated_data):
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs["username"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        attrs["user"] = user
        return attrs


class UserSkillSerializer(serializers.ModelSerializer):
    skill_id = serializers.PrimaryKeyRelatedField(source="skill", queryset=Skill.objects.all())
    skill_name = serializers.CharField(source="skill.name", read_only=True)

    class Meta:
        model = UserSkill
        fields = ("id", "skill_id", "skill_name", "direction", "level")
        read_only_fields = ("id", "skill_name")

    def create(self, validated_data):
        try:
            return UserSkill.objects.create(user=self.context["request"].user, **validated_data)
        except Exception as exc:
            from django.db import IntegrityError
            if isinstance(exc, IntegrityError):
                raise serializers.ValidationError("This skill is already on that list.") from exc
            raise


class ProfileSerializer(serializers.ModelSerializer):
    teach_skills = serializers.SerializerMethodField()
    learn_skills = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "bio", "teach_skills", "learn_skills")
        read_only_fields = ("id", "username", "email", "teach_skills", "learn_skills")

    def get_teach_skills(self, user):
        return UserSkillSerializer(user.user_skills.filter(direction=UserSkill.Direction.TEACH), many=True).data

    def get_learn_skills(self, user):
        return UserSkillSerializer(user.user_skills.filter(direction=UserSkill.Direction.LEARN), many=True).data
