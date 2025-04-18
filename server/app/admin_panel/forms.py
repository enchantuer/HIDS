from django.forms import ModelForm
from .models import UserModel


class UserModelForm(ModelForm):
    class Meta:
        model = UserModel
        fields = ["username", "email", "password1", "password2"]