from django.db import IntegrityError
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from photo_site.forms import SignupForm, LoginForm

# Create your views here.
def test_layout(request):
    return render(request, 'photos/test.html')

def index(request):
    user = User.objects.filter(email='eric@eric.com')
    context = {'user': user}
    return render(request, 'photos/index.html')

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

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/main/photos/')
                else:
                    messages.error(request, 'Account is not active')
        else:
            messages.error(request, 'Invalid email/password')
    else:
        form=LoginForm()
    return render(request, 'photos/login.html', {'form': form})


"""
# creates holding page for url /photos/253/home
# any ID number returned
def user_page(request, user_id):
    return HttpResponse('User ID %s home page' % user_id)
"""