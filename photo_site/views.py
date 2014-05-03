from django.db import IntegrityError
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from photo_site.models import Images
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from photo_site.forms import SignupForm, LoginForm, UploadFileForm
import boto
from boto.s3.key import Key

def test_layout(request):
    return render(request, 'photos/test.html')

def index(request):
    return render(request, 'photos/index.html')

@login_required(login_url='/main/login/')
def user_page(request, username):
    username = request.user.username
    user_images = Images.objects.filter(user__username=request.user.username)
    context = {'user_images': user_images}
    return render(request, 'photos/user_page.html', context)

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
                    return redirect('user_page', username=request.user.username)
                else:
                    messages.error(request, 'Account is not active')
            else:
                messages.error(request, 'Invalid username/password')
    else:
        form=LoginForm()
    return render(request, 'photos/login.html', {'form': form})

@login_required(login_url='/main/login/')
def upload_image(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            filename = request.FILES['file'].name
            file_title = form.cleaned_data['title']

            # restrict file types to jpg gif or jpeg
            if filename[-3:].lower() in ['jpg', 'gif'] or filename[-4:].lower() in ['jpeg']:
                image_url = 'https://s3.amazonaws.com/photosite-django/users/%s/photos/%s' % (request.user.username, filename)
                check_url = Images.objects.filter(file_url=image_url).exists()
        
                if check_url is False:
                    # connect and upload to s3
                    conn = boto.connect_s3(settings.ACCESS_KEY, settings.PASS_KEY)
                    bucket = conn.create_bucket('photosite-django')
                    k = Key(bucket)
                    folder_name = 'users/%s/photos/%s' % (request.user.username, filename) # create s3 folder
                    k.key = folder_name
                    k.set_contents_from_string(file.read())
                    k.set_acl('public-read')

                    add_to_db = User.objects.get(username='eric')
                    add_to_db.images_set.create(file_url=image_url, title=file_title)
                    add_to_db.save()
                    messages.success(request, 'Image added')
                    return HttpResponseRedirect('/main/photos/')
                else:
                    messages.error(request, 'File name already exists. Please rename or choose a different image')
            else:
                messages.error(request, 'Invalid file type. Please use .jpg, .gif, or .jpeg')
    else:
        form = UploadFileForm()
    return render(request, 'photos/upload.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out')
    return redirect('index')

def image_page(request, username, items_id):
    return HttpResponse('Username %s item id %s' % (username, items_id))


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