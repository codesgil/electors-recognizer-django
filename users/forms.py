from django import forms
from .models import User, Profile
from django.core.validators import RegexValidator


class LogOutForm(forms.Form):
    refresh = forms.CharField(required=True)


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=True, min_length=3, max_length=100)
    last_name = forms.CharField(required=False, min_length=3, max_length=100)
    phone = forms.CharField(required=True, min_length=9, max_length=12, validators=[
        RegexValidator('^((237|00)?(6([5-9][0-9]{7}))|((242|243)[0-9]{6}))$',
                       'Enter a valid phone format ((237 ou 00)xxxxxxxxx)')
    ])
    email = forms.CharField(required=False, min_length=5, max_length=100)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone', 'email']


class UserForm(forms.ModelForm):
    username = forms.CharField(required=True, min_length=3, max_length=50)
    password = forms.CharField(required=True, widget=forms.PasswordInput, min_length=3, max_length=50)

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        password = self.cleaned_data["password"]
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'is_active', 'role', 'password']


class UserUpdateForm(forms.ModelForm):
    # Feel free to add the password validation field as on UserCreationForm
    password = forms.CharField(required=False, widget=forms.PasswordInput, min_length=3, max_length=15)

    class Meta:
        model = User
        fields = ('is_active', 'role')

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        password = self.cleaned_data["password"]
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
