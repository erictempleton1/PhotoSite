from django import forms

class SignupForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class ChangePWForm(forms.Form):
    old_pw = forms.CharField(widget=forms.PasswordInput)
    new_pw = forms.CharField(widget=form.PasswordInput)
    check_new = forms.CharField(widget=forms.PasswordInput)