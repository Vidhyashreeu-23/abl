from django.contrib import admin
from .models import Event, EventRegistration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'club', 'start_datetime', 'location')
    list_filter = ('club', 'is_online')
    search_fields = ('title', 'description', 'location')


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'registered_at')
    search_fields = ('event__title', 'user__username')
