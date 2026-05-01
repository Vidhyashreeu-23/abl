from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Skill, Interest


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {'fields': ('bio', 'profile_picture', 'college', 'graduation_year', 'skills', 'interests')}),
    )
    list_display = ('username', 'email', 'college', 'graduation_year', 'is_staff')
    filter_horizontal = ('skills', 'interests')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ('name',)
