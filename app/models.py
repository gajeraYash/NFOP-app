from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from datetime import datetime
from django.core.validators import FileExtensionValidator
from NFOP.storages import FormStorage

# Create your functions here.

def upload_path(instance, filename):
    _now = datetime.now()
    modelInfo = "Error"
    if (instance._meta.model.__name__ == "PoliceUpload"):
        modelInfo = "police"
    elif (instance._meta.model.__name__ == "MemberUpload"):
        modelInfo = "member"
    date = _now.strftime("%Y-%m-%d")
    time = _now.strftime("%I.%M.%S.%p")
    return '{0}/{1}/{2}_{3}/{4}'.format(instance.user.username,modelInfo, date, time, filename)

def form_storage_path(instance, filename):
    _now = datetime.now()
    ext = filename.split('.')[-1]
    name = filename.split('.')[0]
    modelInfo = instance.get_group_display()
    date = _now.strftime("%Y-%m-%d")
    return '{0}/{1}_{2}.{3}'.format(modelInfo, name, date, ext)

# Create your models here.
class UserProfile (models.Model):
    user = models.OneToOneField(User, default="", on_delete=CASCADE)
    address_1 = models.CharField(max_length=128)
    address_2 = models.CharField(max_length=128, blank=True)

    city = models.CharField(max_length=64)
    state = models.CharField(max_length=24)
    zip_code = models.CharField(max_length=5)

    phone_number = models.CharField(max_length=14)

    def __str__(self):
        return ( '('+self.user.username + ')\n' 
        + self.user.first_name + ' '  + self.user.last_name 
        + '\nassociated address:\n' 
        + self.address_1 + '\n'
        + self.address_2 + '\n'
        + self.city + ', ' + self.state + ' ' + self.zip_code)
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

class UserStatus(models.Model):
    UNVERIFIED = 'UVER'
    MEMBER = 'MEMB'
    POLICE = 'POLI'

    STATUS_CHOICES = [
        (UNVERIFIED, 'Unverified'),
        (MEMBER, 'Member'),
        (POLICE, 'Police'),
    ]
        
    user = models.OneToOneField(User, on_delete=CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, default=UNVERIFIED, max_length=4)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + ' is a ' +self.status + ' status.'

    def is_authorized(self):
        return self.status in {self.POLICE, self.ACTIVE} 
    
    class Meta:
        verbose_name = 'User Status'
        verbose_name_plural = 'User Status'

class MailList(models.Model):
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    email = models.CharField(max_length=254)

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        return super(MailList, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'MailList Request'
        verbose_name_plural = 'MailList Requests'

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' - ' + self.email


class FeedbackContact(models.Model):
    full_name = models.CharField(max_length=200,default="")
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        return super(FeedbackContact, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Feedback Contact Request"
        verbose_name_plural = "Feedback Contact Requests"

    def __str__(self):
        return self.full_name + ' - ' + self.subject


class PoliceUpload(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    form = models.FileField(upload_to=upload_path, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Police Upload"
        verbose_name_plural = "Police Uploads"
    
    def __str__(self):
        return self.user.username + ' - ' + str('{0}'.format(self.date.strftime("%m/%d/%Y")))

class MemberUpload(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    form = models.FileField(upload_to=upload_path)
    frontDL = models.ImageField(upload_to=upload_path)
    backDL = models.ImageField(upload_to=upload_path)
    carReg = models.ImageField(upload_to=upload_path)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Member Upload"
        verbose_name_plural = "Member Uploads"

    def __str__(self):
        return self.user.username + ' - ' + str('{0}'.format(self.date.strftime("%m/%d/%Y")))
class Links(models.Model):
    name = models.CharField(max_length=200)
    link = models.TextField(max_length=500)

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'
    
    def __str__(self):
        return self.name

class DownloadForms(models.Model):
    MEMBER = 'MEMB'
    POLICE = 'POLI'

    GROUP_CHOICE = [
        (MEMBER, 'Member'),
        (POLICE, 'Police'),
    ]
    group = models.CharField(choices=GROUP_CHOICE, primary_key=True, max_length=4)
    form = models.FileField(storage=FormStorage(),upload_to=form_storage_path)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Download Form'
        verbose_name_plural = 'Download Forms'

    def __str__(self):
        return self.group + ' - ' + str(self.date.strftime("%Y-%m-%d"))
