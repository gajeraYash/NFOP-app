from django.urls import path
from django.urls.base import reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf import settings


app_name = 'app'  # here for namespacing of urls.

urlpatterns = [
    # Index Page (HOME)
    path('', views.index, name="index"),

    # About Page
    path('about', TemplateView.as_view(template_name='app/about.html'), name="about"),
    
    # Contact Us Page
    path('contact', views.contact, name="contact"),

    # Register Page
    path('signup', views.signup, name="signup"),

    # Login/Logout Page
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),

    # Donate Page
    path('donate', TemplateView.as_view(template_name='app/donate.html'), name="donate"),

    # Events Page
    path('events', views.events, name="events"),

    # Subscribe 
    path('subscribe', views.subscribe_email, name='subscribe_email'),

    # Members Area Pages
    path('member', views.member, name="member"),
    path('member/edit', views.editinfo, name="edit_member"),
    path('member/forms', views.forms, name="forms"),
    path('member/upload/member', views.upload_member, name="upload_member"),
    path('member/upload/police', views.upload_police, name="upload_police"),

    # Account Changes Pages
    path('password/forgot', views.password_forgot, name="forgot_password"),
    path('password/forgot/done', auth_views.PasswordResetDoneView.as_view(template_name='app/password/password_forgot_done.html'), name="forgot_password_done"),
    path('password/reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='app/password/password_reset.html', success_url=reverse_lazy('app:reset_password_done')), name="reset_password"),
    path('password/reset/done', auth_views.PasswordResetCompleteView.as_view(template_name='app/password/password_reset_done.html',), name="reset_password_done"),
    path('username/forgot', views.username_forgot, name="forgot_username")
    
]

if settings.DEBUG:
    # Test Page (Replace Template name with custom html to view the page)
    urlpatterns.append(path('test/', TemplateView.as_view(template_name='app/index.html'), name="test"))