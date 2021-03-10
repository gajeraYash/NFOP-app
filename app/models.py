from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

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
    VERIFIED = 'VERI'
    ACTIVE = 'ACTI'
    POLICE = 'POLI'

    STATUS_CHOICES = [
        (UNVERIFIED, 'Unverified'),
        (VERIFIED, 'Verified'),
        (ACTIVE, 'Active'),
        (POLICE, 'Police'),
    ]
        
    user = models.OneToOneField(User, on_delete=CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, default=UNVERIFIED, max_length=4)

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
