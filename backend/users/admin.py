from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User



@admin.register(User)
class TradeSwapUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("TradeSwap profile", {"fields": ("bio",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("TradeSwap profile", {"fields": ("email", "bio")} ),)
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
