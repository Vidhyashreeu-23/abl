from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Interest, Skill


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    college = forms.CharField(required=False, max_length=255)
    graduation_year = forms.IntegerField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'college', 'graduation_year', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = CustomUser
        fields = ['bio', 'profile_picture', 'skills', 'interests', 'college', 'graduation_year']
