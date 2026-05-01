from django.db import models
from django.contrib.auth import get_user_model
from clubs.models import Club

User = get_user_model()


class Review(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('club', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} review of {self.club.name}'
