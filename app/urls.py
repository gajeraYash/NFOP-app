from django.urls import path
from django.urls.base import reverse_lazy
from . import views
from django.contrib.auth import views as auth_views


app_name = 'app'  # here for namespacing of urls.

urlpatterns = [
    # Index Page (HOME)
    path('', views.index, name="index"),

    # Test Page
    path('test/', views.test, name="test"),
    
    # About Page
    path('about', views.about, name="about"),
    
    # Contact Us Page
    path('contact', views.contact, name="contact"),

    # Register Page
    path('signup', views.signup, name="signup"),

    # Login/Logout Page
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),

    # Donate Page
    path('donate', views.donate, name="donate"),

    # Members Area Pages
    path('member', views.member, name="member"),

    # Account Changes Pages
    path('password/forgot', views.password_forgot, name="forgot_password"),
    path('password/forgot/done', auth_views.PasswordResetDoneView.as_view(template_name='app/password/password_forgot_done.html'), name="forgot_password_done"),
    path('password/reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='app/password/password_reset.html', success_url=reverse_lazy('app:reset_password_done')), name="reset_password"),
    path('password/reset/done', auth_views.PasswordResetCompleteView.as_view(template_name='app/password/password_reset_done.html',), name="reset_password_done"),
    path('username/forgot', views.username_forgot, name="forgot_username")
    
]

