from django.contrib import admin
from .models import Category, Club, Membership


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_by', 'is_approved', 'member_count')
    list_filter = ('category', 'is_approved')
    search_fields = ('name', 'description')


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'club', 'role', 'joined_at')
    list_filter = ('role',)
    search_fields = ('user__username', 'club__name')
