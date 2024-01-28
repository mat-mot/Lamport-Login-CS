from django import forms
from User.models import User


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'name': 'password'}))
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'name': 'confirm_password'}))

    class Meta:
        model = User
        fields = ['username']

    def check_password(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("confirm_password")
        return password1 != password2

    def clean(self):
        cleaned_data = super().clean()
        if self.check_password():
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data


class UserSigninForm(forms.Form):

    username = forms.CharField(label='Username', widget=forms.TextInput())
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    repetitions = forms.IntegerField(widget=forms.HiddenInput, initial=10)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if username and password:
            user = User.objects.filter(username=username).first()
            if not user:
                raise forms.ValidationError("Invalid username or password.")
        return cleaned_data
