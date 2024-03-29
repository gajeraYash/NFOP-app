from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from datetime import datetime
from app.forms import *
from app.models import *
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

# Create your views here.

def index(request):
    return render(request,"app/index.html", {'numIMG' : range(1,11)})

def events(request):
    return render(request,"app/events.html")

def contact(request):
    if request.method == 'POST':
        contact_form = FeedbackContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            admins = [reciever for reciever in (User.objects.filter(groups__name='contactRequest').values_list('email', flat=True))]
            print(admins)
            full_name = request.POST.get('full_name', 'NULL')
            email = request.POST.get('email', 'NULL')
            subject = request.POST.get('subject', 'NULL')
            message = request.POST.get('message', 'NULL')
            context = { 
                'title': 'Contact Request', 
                'full_name': full_name, 
                'email': email, 
                'subject': subject, 
                'message': message, 
                'date': datetime.now()
                }
            html_content = render_to_string('email/contact_email.html', context)
            text_content = get_template('email/contact_email.txt').render(context)
            email_subject = "CONTACT REQUEST: " + subject
            email = EmailMultiAlternatives(
                email_subject,
                text_content,
                'NewarkFOP12 <{0}>'.format(settings.EMAIL_HOST_USER),
                admins,
                reply_to=[email]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
            messages.success(request, 'Contact form has been submitted.')
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

def password_forgot(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['username'].lower()
            associated_users = User.objects.filter(username=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Reset Password - NewarkFOP12"
                    email_template_name = "email/reset_password.html"
                    textemail_template_name = "email/reset_password.txt"
                    if settings.DEBUG:
                        domain = '127.0.0.1:8000'
                        protcolSSL = 'http'
                    else:
                        domain = 'www.newarkfop12.com'
                        protcolSSL = 'https'
                    context = {
                        'domain': domain,
                        'title': 'Newark Fraternal Order of Police',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': protcolSSL,
                    }
                    html_content = render_to_string(email_template_name, context)
                    text_content = get_template(textemail_template_name).render(context)
                    template_email = EmailMultiAlternatives(
                        subject,
                        text_content,
                        'Do Not Reply <{0}>'.format(settings.EMAIL_HOST_USER),
                        [user.email]
                    )
                    template_email.attach_alternative(html_content, "text/html")
                    template_email.send()
            return HttpResponseRedirect(reverse('app:forgot_password_done'))
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'app/password/password_forgot.html', {'form': form})

def username_forgot(request):
    if request.method == 'POST':
        form = ForgotUsernameForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['email'].lower()
            user = User.objects.filter(email=data)
            if user.exists():
                subject = "Forgot Username - NewarkFOP12"
                email_template_name = "email/forgot_username.html"
                textemail_template_name = "email/forgot_username.txt"
                context = {
                    'title': 'Newark Fraternal Order of Police',
                    'username' : user[0].username,
                }
                html_content = render_to_string(email_template_name, context)
                text_content = get_template(textemail_template_name).render(context)
                template_email = EmailMultiAlternatives(
                    subject,
                    text_content,
                    'Do Not Reply <{0}>'.format(settings.EMAIL_HOST_USER),
                    [user[0].email]
                )
                template_email.attach_alternative(html_content, "text/html")
                template_email.send()
        return HttpResponseRedirect(reverse('app:forgot_username_done'))
    else:
        form = ForgotUsernameForm()
    
    return render(request, 'app/account/username_forgot.html', {'form': form})

@login_required
def member(request):
    return render(request, 'app/member/member.html')
    
@login_required
def forms(request):
    formMember = DownloadForms.objects.filter(group='MEMB')
    formPolice = DownloadForms.objects.filter(group='POLI')
    return render(request, 'app/member/forms.html',{'formMember': formMember, 'formPolice': formPolice })

@login_required
def upload_member(request):
    return render(request, 'app/member/member_upload.html')
    
@login_required
def upload_police(request):
    if request.method == "POST":
        uploadForm = UploadPoliceForm(request.POST, request.FILES)
        if uploadForm.is_valid():
            form = uploadForm.save(commit=False)
            form.user = request.user
            form.save()
            messages.success(request, 'Files have been uploaded successfully')
    else:
        uploadForm = UploadPoliceForm()
    return render(request, 'app/member/police_upload.html', {'form': uploadForm})

@login_required
def upload_member(request):
    if request.method == "POST":
        uploadForm = UploadMemberForm(request.POST, request.FILES)
        if uploadForm.is_valid():
            form = uploadForm.save(commit=False)
            form.user = request.user
            form.save()
            messages.success(request, 'Files have been uploaded successfully')
    else:
        uploadForm = UploadMemberForm()
    return render(request, 'app/member/member_upload.html', {'form': uploadForm})

@csrf_exempt
def subscribe_email(request):
    if request.method == "POST" and request.is_ajax():
        subscribeform = MailListForm(request.POST)
        if subscribeform.is_valid():
            subscribeform.save()
            messages.success(request, 'Email has succesfully been subscribed')
        return render(request, 'app/partials/subscribe.html', {'form': subscribeform})
    elif request.method == "GET" and request.is_ajax():
        subscribeform = MailListForm()
        return render(request, 'app/partials/subscribe.html', {'form': subscribeform})
@login_required
def editinfo(request):
    if request.method == 'POST':
        user_info_form = EditUserInfoForm(request.POST, instance= request.user)
        user_profile_form = EditUserProfileForm(request.POST, instance= request.user.userprofile)
        if (user_info_form.is_valid() and user_profile_form.is_valid()):
            user_info_form.save()
            user_profile_form.save()
            return HttpResponseRedirect(reverse("app:member"))
        else:
            print("error while editing profile")
    else:
        user_info_form = EditUserInfoForm(instance= request.user)
        user_profile_form = EditUserProfileForm(instance= request.user.userprofile)
    return render(request, 'app/member/edit_member.html', {"profile_info": user_profile_form, "user_info": user_info_form})


    