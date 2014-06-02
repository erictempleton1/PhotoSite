from django import forms

class SignupForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_again = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class ChangePWForm(forms.Form):
    old_pw = forms.CharField(widget=forms.PasswordInput)
    new_pw = forms.CharField(widget=forms.PasswordInput)
    check_new = forms.CharField(widget=forms.PasswordInput)

class ChangeEmailForm(forms.Form):
    check_password = forms.CharField(widget=forms.PasswordInput)
    old_email = forms.EmailField(max_length=100)
    new_email = forms.EmailField(max_length=100)