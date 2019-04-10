from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class UserCustomCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'email', ]

class UserCustomChangeForm(UserChangeForm):
    class Meta:
        # https://docs.djangoproject.com/en/2.2/ref/contrib/auth/
        model = User
        fields = ['email', 'first_name', 'last_name',]