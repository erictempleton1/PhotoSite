from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    user = User.objects.get(email='eric@eric.com')
    return HttpResponse('Hello, %s!' % user.username)

# creates holding page for url /photos/253/home
# any ID number returned
def user_page(request, user_id):
    return HttpResponse('User ID %s home page' % user_id)