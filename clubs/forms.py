from django import forms
from .models import Club


class ClubForm(forms.ModelForm):
    social_links = forms.JSONField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
        help_text='Enter a JSON object for social links, e.g. {"instagram": "https://...", "website": "https://..."}',
    )

    class Meta:
        model = Club
        fields = ['name', 'description', 'logo', 'cover_image', 'category', 'social_links']
