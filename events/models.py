from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from clubs.models import Club

User = get_user_model()


class Event(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=220)
    description = models.TextField()
    banner = models.ImageField(upload_to='event_banners/', blank=True, null=True)
    location = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    max_attendees = models.IntegerField(null=True, blank=True)
    is_online = models.BooleanField(default=False)
    meeting_link = models.URLField(blank=True)

    class Meta:
        ordering = ['start_datetime']

    def __str__(self):
        return f'{self.title} ({self.club.name})'

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk': self.pk})

    @property
    def attendee_count(self):
        return self.registrations.count()


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_registrations')
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')
        ordering = ['registered_at']

    def __str__(self):
        return f'{self.user.username} registered for {self.event.title}'
