from django.db import IntegrityError
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from photo_site.forms import SignupForm, LoginForm, UploadFileForm

def test_layout(request):
    return render(request, 'photos/test.html')

def index(request):
    return render(request, 'photos/index.html')

@login_required(login_url='/main/login/')
def upload_image(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/main/photos/')
    else:
        form = UploadFileForm()
    return render(request, 'photos/upload.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            check_username = User.objects.filter(username=username)
            check_email = User.objects.filter(email=email)

            if check_email.exists():
                messages.error(request, 'Email already in use')
            if len(password) < 4:
                messages.error(request, 'Passwords must be 4 or more characters')
            else:
                try:
	                user = User.objects.create_user(username, email, password)
	                user.save()
	                messages.success(request, 'Account created. Please login')
                except IntegrityError:
                    # above error thrown if username exists
                    messages.error(request, 'Username already in use')
                return redirect('/main/login/')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/main/photos/')
                else:
                    messages.error(request, 'Account is not active')
            else:
                messages.error(request, 'Invalid username/password')
    else:
        form=LoginForm()
    return render(request, 'photos/login.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out')
    return redirect('/main/photos/')


"""
>>> import boto
>>> conn = boto.connect_s3(aws_access_key_id="", aws_secret_access_key="")
>>> bucket = conn.create_bucket('photosite-django')
>>> from boto.s3.key import Key
>>> k = Key(bucket)
>>> k.key = 'user/photos'
>>> k.set_contents_from_filename('/Users/erictempleton/Desktop/Arsenal_2.jpg')
304404
>>> k.get_contents_to_filename('/Users/erictempleton/Desktop/Arsenal_2.jpg')
>>> bucket.set_acl('public-read')
"""

"""
# creates holding page for url /photos/253/home
# any ID number returned
def user_page(request, user_id):
    return HttpResponse('User ID %s home page' % user_id)
"""