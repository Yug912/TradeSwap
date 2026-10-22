from django.contrib import admin
from .models import Skill, UserSkill



@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ("user", "skill", "direction", "level")
    list_filter = ("direction", "level")
    search_fields = ("user__username", "skill__name")
