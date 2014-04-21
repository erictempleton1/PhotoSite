from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here.
def test_layout(request):
    return render(request, 'photos/test.html')

def index(request):
    user = User.objects.filter(email='eric@eric.com')
    context = {'user': user}
    return render(request, 'photos/index.html')

def login(request):
    return render(request, 'photos/login.html')


"""
# creates holding page for url /photos/253/home
# any ID number returned
def user_page(request, user_id):
    return HttpResponse('User ID %s home page' % user_id)
"""