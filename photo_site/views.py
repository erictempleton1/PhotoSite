from django.db import IntegrityError
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from photo_site.models import Images
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from photo_site.forms import SignupForm, LoginForm, UploadFileForm, ChangePWForm, ChangeEmailForm, ImageURLForm
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
            file_form = UploadFileForm(request.POST, request.FILES)
            url_form = ImageURLForm(request.POST, request.FILES)
            if file_form.is_valid():
                filename = request.FILES['file'].name
                file_title = file_form.cleaned_data['title']

                # appends id to filename to check if image exists for a user
                user_filename = '{0}_{1}'.format(request.user.id, filename)
                filename_exists = Images.objects.filter(filename=user_filename).exists()
                
                # checks if image already exists
                check_url = Images.objects.filter(file_url=image_url).exists()

                # returns image count
                image_count = user_images.count()

                # check if user exists in the group
                user = User.objects.get(username=request.user.username)
                group_check = user.groups.filter(name = 'Premium').exists()

                if image_count <= settings.IMAGE_LIMIT or group_check:

                    if filename_exists is False:

                        # save title, file url, and thumb url to db via set
                        filename_to_db = User.objects.get(username=request.user.username)
                        filename_to_db.images_set.create(orig_filename=filename, title=file_title, 
                                                         image=request.FILES['file'], user_filename=user_filename,)
                        filename_to_db.save()

                        messages.success(request, 'Image added')
                        return redirect('user_page', username=request.user.username)
                    else:
                        messages.error(request, 'File name already exists. Please rename or choose a different image')
                else:
                    messages.error(request, 'You have reached your upload limit. Please upgrade or remove a few images.')

            elif url_form.is_valid():
                pass
    else:
        file_form = UploadFileForm()
        url_form = ImageURLForm()

    # splits s3 file url at ?, and slices off extra appends on url
    # the result is then appended to the cloudfront url
    url_split = [images.thumbnail.url.split('?')[0][46:] for images in user_images]
    cloudfront_append = ['{0}{1}'.format(settings.CLOUDFRONT_URL, images) for images in url_split]

    context = {'file_form': file_form, 'cloudfront_append': cloudfront_append,
                'username': username, 'url_form': url_form}
                
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
        
            if len(password) >= 4:
                if password == password_again:
                    if check_username.count() == 0 and check_email.count() == 0:
                        user = User.objects.create_user(username, email, password)
                        user.save()
                        messages.success(request, 'Account created. Please login')
                        return redirect('/login/')
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
    context = {'form': form}
    return render(request, 'photos/login.html', context)

@login_required(login_url='/login/')
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
    context = {'form': form}
    return render(request, 'photos/change_pw.html', context)

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def image_page(request, username, items_id):
    image_id = Images.objects.get(id=items_id)
    image_url = '{0}{1}'.format(settings.CLOUDFRONT_URL, image_id.image.url.split('?')[0][46:] )
    #image_url = image_id.file_url
    context = {'image_url': image_url}
    return render(request, 'photos/image_page.html', context)

@login_required(login_url='/login/')
def update_image(request):
    username = request.user.username
    user_images = Images.objects.filter(user__username=username)

    try:
        # return number of images
        image_count = user_images.count()

        # returns most recent object, date in this case
        # indexerror if no images uploaded yet
        user_recent = Images.objects.filter(user__username=username).order_by('-id')[0]
        recent_date = user_recent.added

    except IndexError:
        # if no images are uploaded yet
        #image_count = 0
        recent_date = 'No images added'

    try:
        # add display for current user group
        user = User.objects.get(username=username)
        user_group = user.groups.all()[0]

    except IndexError:
        # if user is not in premium group they are in "free tier"
        user_group = 'Free Tier ({0} images allowed)'.format(settings.IMAGE_LIMIT)

    context = {'user_images': user_images, 'username': username,
                'image_count': image_count, 'recent_date': recent_date,
                'user_group': user_group}
    
    return render(request, 'photos/update.html', context)


@login_required(login_url='/login/')
def remove_image(request, image_id):

    # connect to s3
    conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    mybucket = conn.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)

    # returns None if key doesn't exist
    # exists = mybucket.get_key('eric/images/2_ChugachMountains.jpg')
    # split drops everything beyond the ?, and slices extra added onto the url
    image = Images.objects.get(id=image_id)
    image_exists = mybucket.get_key(('{0}').format(image.image.url.split('?')[0][47:]))
    thumb_exists = mybucket.get_key(('{0}').format(image.thumbnail.url.split('?')[0][47:]))

    if image_exists is not None and thumb_exists is not None:
        # deletes from s3
        image_exists.delete()
        thumb_exists.delete()

        # deletes image and thumb info from db
        image.delete()
        messages.success(request, 'Image removed')
    else:
        messages.error(request, 'Sorry, something has gone wrong.')

    return redirect('update_image')
