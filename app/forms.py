from django import forms

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from app.models import FeedbackContact, MailList, MemberUpload, PoliceUpload, UserProfile

class UsernameLowField(forms.CharField):
    def to_python(self, value):
        return value.lower()
class EmailLowField(forms.EmailField):
    def to_python(self, value):
        return value.lower()

class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=35, required=True)
    last_name = forms.CharField(max_length=35, required=True)
    email = EmailLowField(max_length=254, required=True, help_text="We will never share your email with anyone else.")
    username = UsernameLowField(max_length=15, min_length=3, required=True, help_text="Username must be between 3 - 15 characters and can contain '_'. ",validators=[
        RegexValidator(
            regex='^(?=.{3,15}$)(?!.*[_]{2})[a-zA-Z0-9_]+$',
            message='Username is invalid!',
            code='invalid_username'
        ),
    ])
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already in use.")
        if User.objects.filter(email=email.lower()).exists():
            raise ValidationError("Email already in use.")
        return self.cleaned_data

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('address_1', 'address_2', 'city', 'state', 'zip_code', 'phone_number')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=15, min_length=3)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username').lower()
        print(username + ' is initiating a login.')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            
            if not user:
                raise forms.ValidationError('Invalid username or password.', code="invalid_uid")
            if not user.is_active:
                raise forms.ValidationError('User status is currently inactive', code="invalid_uemail")

        return super(LoginForm,self).clean(*args, **kwargs)

class MailListForm(forms.ModelForm):
    class Meta:
        model = MailList
        fields = ('email', 'first_name', 'last_name')
    
    def clean(self):
        email = self.cleaned_data.get('email')
        if MailList.objects.filter(email=email.lower()).exists():
            raise ValidationError("Email already subscribed for mailing list.")
        return self.cleaned_data

class FeedbackContactForm(forms.ModelForm):
    class Meta:
        model = FeedbackContact
        fields = ('full_name', 'email', 'subject', 'message')

class ForgotPasswordForm(forms.Form):
    username = forms.CharField(max_length=15, label="Username")

class ForgotUsernameForm(forms.Form):
    email = EmailLowField(max_length=254, label="Email")

class UploadPoliceForm(forms.ModelForm):
    class Meta:
        model = PoliceUpload
        fields = ('form',)

class UploadMemberForm(forms.ModelForm):
    class Meta:
        model = MemberUpload
        fields = ('form','frontDL', 'backDL','carReg',)

class EditUserInfoForm(forms.ModelForm):
    first_name = forms.CharField(max_length=35, required=True)
    last_name = forms.CharField(max_length=35, required=True)
    email = EmailLowField(max_length=254, required=True)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
    
    def clean(self):
        email = self.cleaned_data.get('email')
        
        if self.instance.pk is not None and self.instance.email == email:
            return self.cleaned_data

        if User.objects.filter(email=email.lower()).exists():
            raise ValidationError("Email already in use.")
        return self.cleaned_data

class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('address_1', 'address_2', 'city', 'state', 'zip_code', 'phone_number')