from django.forms import ModelForm
from .models import Submission
from .models import User
from django.contrib.auth.forms import UserCreationForm


class EditUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'avatar', 'bio', 'linkedin', 'website', 'github', 'facebook', 'twitter']

class SubmissionForm(ModelForm):
    class Meta:
        model = Submission
        fields = ['details']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'password1', 'password2']
