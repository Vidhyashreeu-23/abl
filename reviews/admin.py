from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('club', 'user', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('club__name', 'user__username', 'comment')
