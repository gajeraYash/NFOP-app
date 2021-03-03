from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from app.forms import *
from app.models import *
# Create your views here.

def index(request):
    return render(request,"app/index.html")

def test(request):
    return render(request,"app/index.html") #Replace Under The Quotes for Custom Test HTML Page

def about(request):
    return render(request,"app/index.html")

def contact(request):
    return render(request, "app/contact.html")
 
def signup(request):
    if request.method == 'POST':
        user_form = SignupForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            status = UserStatus(user = user)
            status.save()
            return HttpResponseRedirect(reverse('app:index'))
        else:
            print('Error Occured')
    else:
        user_form = SignupForm()
        profile_form = UserProfileForm()
    return render(request, 'app/signup.html', {'user_form': user_form,
                                                'profile_form': profile_form,})

def login(request):
    return render(request, "app/index.html")

def logout(request):
    return render(request, "app/index.html")

def social_media(request):
    return render(request, "app/index.html")

def donate(request):
    return render(request, "app/index.html")