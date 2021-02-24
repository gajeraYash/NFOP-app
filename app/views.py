from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request,"app/index.html")

def test(request):
    return render(request,"app/index.html") #Replace Under The Quotes for Custom Test HTML Page

def about(request):
    return render(request,"app/index.html")

def contact(request):
    return render(request, "app/index.html")
 
def register(request):
    return render(request, "app/index.html")

def login(request):
    return render(request, "app/index.html")

def logout(request):
    return render(request, "app/index.html")

def social_media(request):
    return render(request, "app/index.html")

def donate(request):
    return render(request, "app/index.html")

