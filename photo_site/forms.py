from django import forms

class SignupForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password_again = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}))

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class UploadFileForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Image Title'}))
    file = forms.FileField()

class ChangePWForm(forms.Form):
    old_pw = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}))
    new_pw = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}))
    check_new = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password Again'}))

class ChangeEmailForm(forms.Form):
    check_password = forms.CharField(widget=forms.PasswordInput)
    old_email = forms.EmailField(max_length=100)
    new_email = forms.EmailField(max_length=100)