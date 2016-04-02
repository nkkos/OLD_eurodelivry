import re

from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

    # NB: you'll need to set auth_user username to VARCHAR(75)
    username = forms.EmailField(label='Email', max_length=75)
    password = forms.CharField(widget=forms.PasswordInput())

    buf_username = None

    def clean_username(self):
        username = self.cleaned_data['username']
        self.buf_username = username
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Such user already exists")

        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if (len(password) < 6 or
                not (re.search('\d', password) and
                     re.search('[A-Za-z]', password))
            ):
            raise forms.ValidationError(
                "Password is weak. It should contain letters and numbers and "
                "be longer than 6 symbols"
            )

        return password

    def full_clean(self):
        super(UserForm, self).full_clean()
        if (self.buf_username and 'username' in self._errors and
                'at most 30' in self._errors['username']):
            del self._errors['username']
            if len(self.buf_username) > 75:
                raise forms.ValidationError(
                    "Ensure this value has at most 75 characters (it has %d)" %
                    (len(self.buf_username), )
                )


class ForgotPasswordForm(forms.Form):
    registered_email = forms.EmailField(max_length=75)


class UserInfoForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=75, required=False)

    # phone = forms.CharField(max_length=20)
    # email_notifications = forms.BooleanField()
    # documents = forms.CharField(max_length=255)
