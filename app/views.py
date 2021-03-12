from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from app.forms import *
from app.models import *
# Create your views here.

def index(request):
    return render(request,"app/index.html", {'numIMG' : range(1,11)})

def test(request):
    return render(request,"app/index.html") #Replace Under The Quotes for Custom Test HTML Page

def about(request):
    return render(request,"app/about.html")

def contact(request):
    if request.method == 'POST':
        contact_form = FeedbackContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, 'Contact form has been submitted.')
            return HttpResponseRedirect(reverse('app:contact'))
    else:
        contact_form = FeedbackContactForm()
    return render(request, "app/contact.html", {'contact_form': contact_form})
 
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

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('app:index'))
    
    return render(request, 'app/signup.html', {'user_form': user_form,
                                                'profile_form': profile_form,})

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username'].lower()
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            auth_login(request,user)
            return HttpResponseRedirect(reverse('app:index'))
        else:
            print("Error: Submitting Request")
    else:
        login_form = LoginForm()
    
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('app:index'))

    return render(request,"app/login.html", {'login_form':login_form})

@login_required
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('app:index'))

def social_media(request):
    return render(request, "app/social_media.html")

def donate(request):
    return render(request, "app/donate.html")

@login_required
def member(request):
    return render(request, "app/member.html")
    
