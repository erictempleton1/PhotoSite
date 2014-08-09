from django.db import IntegrityError
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from photo_site.models import Images
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from photo_site.forms import SignupForm, LoginForm, UploadFileForm, ChangePWForm, ChangeEmailForm
from django.core.urlresolvers import reverse
from django.contrib.auth.views import password_reset, password_reset_confirm
import boto
from boto.s3.key import Key
from boto.s3.connection import Bucket, Key


def index(request):
    # queries most recent images
    # also can return username via image.user.username in template
    # change recent_images slice to add or subtract amount of images shown
    recent_images = Images.objects.all().select_related().order_by('-added')[:100]
    context = {'recent_images': recent_images}
    return render(request, 'photos/index.html', context)

def user_page(request, username):
    username = username
    user_images = Images.objects.filter(user__username=username)

    # adds image upload form to user's page
    if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                filename = request.FILES['file'].name
                file_title = form.cleaned_data['title']
                
                # creates cloudfront file url with lowercase ext from model
                image_url = 'http://d1zl0ln7uechsy.cloudfront.net/photos/%s' % (filename)
                
                # splits filename at . and lowercases extension to fit same extension pattern
                # applied at the thumb save model.
                split_filename = filename.split('.')
                filename_lower = '%s_%s.%s' % (User.objects.make_random_password(), split_filename[0],
                                                split_filename[-1].lower())

                # creates cloudfront thumb url using filename with lowercase extension
                thumbnail_url = 'http://d1zl0ln7uechsy.cloudfront.net/thumbnails/%s%s' % ('thumb_', filename_lower)
                
                check_url = Images.objects.filter(file_url=image_url).exists()
                check_thumb = Images.objects.filter(thumb_url=thumbnail_url).exists()
            
                if check_url is False:

                    # save title, file url, and thumb url to db via set
                    filename_to_db = User.objects.get(username=request.user.username)
                    filename_to_db.images_set.create(filename=filename_lower, file_url=image_url,
                                                        title=file_title, thumb_url=thumbnail_url,
                                                        image=request.FILES['file'])
                    filename_to_db.save()

                    messages.success(request, 'Image added')
                    return redirect('user_page', username=request.user.username)
                else:
                    messages.error(request, 'File name already exists. Please rename or choose a different image')
    else:
        form = UploadFileForm()
    return render(request, 'photos/user_page.html', {'form': form, 'user_images': user_images, 'username': username})

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
        
            if len(password) >= 4:
                if password == password_again:
                    if check_username.count() == 0 and check_email.count() == 0:
                        user = User.objects.create_user(username, email, password)
                        user.save()
                        messages.success(request, 'Account created. Please login')
                        return redirect('/main/login/')
                    else:
                        messages.error(request, 'Username/Email already in use')
                else:
                    messages.error(request, 'Please enter matching passwords')
            else:
                messages.error(request, 'Passwords must be 4 characters or more')
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
def change_email(request):
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            username = request.user.username
            check_pw = form.cleaned_data['check_password']
            old_email = form.cleaned_data['old_email']
            new_email = form.cleaned_data['new_email']
            user_check = authenticate(username=username, password=check_pw)
            if user_check is not None:
                check_email = User.objects.filter(email=new_email)
                if check_email.exists():
                    messages.error(request, 'Email already exists')
                else:
                    user = User.objects.get(username=username)
                    user.email = new_email
                    user.save()
                    messages.success(request, 'Email address changed')
            else:
                messages.error(request, 'Invalid password')
    else:
        form = ChangeEmailForm()
    return render(request, 'photos/change_email.html', {'form': form})

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
    conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket('photosite-django')
    for key in bucket.list():
        if key.name == image_url[42:]:
            key.delete()

    image_get = Images.objects.get(id=image_id)
    image_get.delete()
    messages.success(request, 'Image removed')
    return redirect('update_image')
