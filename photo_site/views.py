from django.db import IntegrityError
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from photo_site.models import Images
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from photo_site.forms import SignupForm, LoginForm, UploadFileForm, ChangePWForm
import boto
from boto.s3.key import Key
from boto.s3.connection import Bucket, Key


def test_layout(request):
    return render(request, 'photos/test.html')

def index(request):
    # queries most recent images
    # also can return username via image.user.username in template
    recent_images = Images.objects.all().select_related().order_by('-added')[:20]
    context = {'recent_images': recent_images}
    return render(request, 'photos/index.html', context)

def user_page(request, username):
    username = username
    user_images = Images.objects.filter(user__username=username)
    context = {'user_images': user_images, 'username': username}
    return render(request, 'photos/user_page.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_again = form.cleaned_data['password_again']

            check_username = User.objects.filter(username=username)
            check_email = User.objects.filter(email=email)

            if check_email.exists():
                messages.error(request, 'Email already in use')
            if len(password) < 4:
                messages.error(request, 'Passwords must be 4 or more characters')
            if password != password_again:
                messages.error(request, 'Please enter matching passwords')
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
    return render(request, 'photos/signup.html', {'form': form})

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
def change_pw(request):
    if request.method == 'POST':
        form = ChangePWForm(request.POST)
        if form.is_valid():
            username = request.user.username
            check_current_pw = request.POST['old_pw']
            new_pw = request.POST['new_pw']
            check_new = request.POST['check_new']
            user = User.objects.get(username=username)
            # authenticate checks if pw is correct
            user_check = authenticate(username=username, password=check_current_pw)
            if user_check is not None:
                if len(new_pw) >= 4:
                    if new_pw == check_new:
                        user.set_password(new_pw)
                        user.save()
                        messages.success(request, 'Password updated')
                        return redirect('user_page', username=username)
                    else:
                        messages.error(request, 'Please enter matching passwords')
                else:
                    messages.error(request, 'Passwords must be 4 or more characters')
            else:
                messages.error(request, 'Invalid password')
    else:
        form = ChangePWForm()
    return render(request, 'photos/change_pw.html', {'form': form})
                

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

                    add_to_db = User.objects.get(username=request.user.username)
                    add_to_db.images_set.create(file_url=image_url, title=file_title)
                    add_to_db.save()
                    messages.success(request, 'Image added')
                    return redirect('user_page', username=request.user.username)
                else:
                    messages.error(request, 'File name already exists. Please rename or choose a different image')
            else:
                messages.error(request, 'Invalid file type. Please use .jpg, .gif, or .jpeg')
    else:
        form = UploadFileForm()
    return render(request, 'photos/upload.html', {'form': form})

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/main/')

def image_page(request, username, items_id):
    image_id = Images.objects.get(id=items_id)
    image_url = image_id.file_url
    context = {'image_url': image_url}
    return render(request, 'photos/image_page.html', {'image_url': image_url})

@login_required(login_url='/main/login/')
def update_image(request):
    username = request.user.username
    user_images = Images.objects.filter(user__username=username)
    context = {'user_images': user_images, 'username': username}
    return render(request, 'photos/update.html', context)


@login_required(login_url='/main/login/')
def remove_image(request, image_id, image_url):
    # only deletes from s3 if image has no spaces
    # does not work very well
    conn = boto.connect_s3(settings.ACCESS_KEY, settings.PASS_KEY)
    bucket = conn.get_bucket('photosite-django')
    for key in bucket.list():
        if key.name == image_url[42:]:
            key.delete()


    image_get = Images.objects.get(id=image_id)
    image_get.delete()
    messages.success(request, 'Image removed')
    return redirect('update_image')
  

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