from django.test import TestCase
from rest_framework.test import APIClient

from skills.models import Skill
from .models import User



class AuthenticationAndProfileTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.skill = Skill.objects.create(name="Python")

    def test_registration_returns_jwt_tokens(self):
        response = self.client.post("/api/register/", {"username": "maya", "email": "maya@example.com", "password": "safe-password-123"}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("access", response.data["tokens"])
        self.assertTrue(User.objects.filter(username="maya").exists())

    def test_authenticated_user_can_manage_profile_skills(self):
        user = User.objects.create_user("maya", "maya@example.com", "safe-password-123")
        self.client.force_authenticate(user)
        profile_response = self.client.put("/api/profile/", {"bio": "I teach Python."}, format="json")
        self.assertEqual(profile_response.status_code, 200)
        create_response = self.client.post("/api/user-skills/", {"skill_id": self.skill.id, "direction": "teach", "level": "advanced"}, format="json")
        self.assertEqual(create_response.status_code, 201)
        self.assertEqual(create_response.data["skill_name"], "Python")
        self.assertEqual(self.client.get("/api/profile/").data["teach_skills"][0]["skill_name"], "Python")
