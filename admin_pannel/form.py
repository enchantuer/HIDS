from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False)  # Facultatif pour l'édition

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:  # Mettre à jour le mot de passe seulement si fourni
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
