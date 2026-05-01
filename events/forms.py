from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    start_datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Event
        fields = ['title', 'description', 'banner', 'location', 'start_datetime', 'end_datetime', 'max_attendees', 'is_online', 'meeting_link']
