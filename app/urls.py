from django.urls import path
from . import views


app_name = 'app'  # here for namespacing of urls.

urlpatterns = [
    path('', views.index, name="home"),
    path('test/', views.test, name="test"),
    
    #About Page
    path('about', views.about, name="about"),
    
    #Contact Us Page
    path('contact', views.contact, name="contact"),

    #Register Page
    path('register', views.register, name="register"),

    #Login/Logout Page
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),

    #Social Media Page
    path('social_media', views.social_media, name="social_media"),

    #Donate Page
    path('donate', views.donate, name="donate"),

]

