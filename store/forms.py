from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=50)
    first_name = forms.CharField(required=True, max_length=20, label='Nombre', help_text='Requerido, máximo 50 caracteres')

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "password1", "password2")

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        if commit:
            user.save()
        return user