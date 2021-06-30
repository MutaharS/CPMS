from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Validate the username (Email)
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Could not find the corresponding user.')
        return username