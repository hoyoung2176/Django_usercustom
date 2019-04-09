from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class UserCustomChangeForm(UserChangeForm):
    class Meta:
        # https://docs.djangoproject.com/en/2.2/ref/contrib/auth/
        model = User
        fields = ['email', 'first_name', 'last_name',]