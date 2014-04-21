from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from photo_site.forms import SignupForm

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

            if check_username.exists():
                messages.error(request, 'Username already in use')
                return HttpResponseRedirect('/signup/')

            if check_email.exists():
                messages.error(request, 'Email already in use')
                return HttpResposeRedirect('/signup/')

            else:
                user = User.objects.create_user(username, email, password)
                user.save()
                messages.success('Account created. Please login')
                return HttpResponseRedirect('/login/')
                
            return HttpResponseRedirect('main/')

    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

    


    return render(request, 'photos/signup.html')

def login(request):
    return render(request, 'photos/login.html')


"""
# creates holding page for url /photos/253/home
# any ID number returned
def user_page(request, user_id):
    return HttpResponse('User ID %s home page' % user_id)
"""