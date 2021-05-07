from django.contrib import admin
from django.contrib.admin.filters import SimpleListFilter
from django.contrib.admin.sites import AdminSite
from app.models import *
from django.urls import reverse
from django.utils.html import format_html

admin.site.site_header = "NewarkFOP12 Admin"
admin.site.site_title = "Admin Page"

# Modify your admin layout here.
class UserStatusAdmin(admin.ModelAdmin):
    search_fields = ['user__first_name', 'user__last_name', 'user__username']
    list_filter = ['status','user__username','user__first_name', 'user__last_name', 'modified']
    list_display = ['user', 'get_user_firstname', 'get_user_lastname','status', 'modified' ]
    list_editable = ['status']

    def get_user_firstname(self, obj):
        return obj.user.first_name
    get_user_firstname.admin_order_field  = 'user__first_name'
    get_user_firstname.short_description = 'First name'

    def get_user_lastname(self, obj):
        return obj.user.last_name
    get_user_lastname.admin_order_field  = 'user__last_name'
    get_user_lastname.short_description = 'Last name'

class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__first_name', 'user__last_name', 'user__username', 'phone_number', 'address_1', 'city', 'state', 'zip_code']
    list_filter = ['user__username','user__first_name', 'user__last_name', 'city','zip_code']
    list_display = ['user', 'get_user_firstname', 'get_user_lastname', 'address_1', 'address_2', 'city','state','zip_code','phone_number']

    def get_user_firstname(self, obj):
        return obj.user.first_name
    get_user_firstname.admin_order_field  = 'user__first_name'
    get_user_firstname.short_description = 'First name'

    def get_user_lastname(self, obj):
        return obj.user.last_name
    get_user_lastname.admin_order_field  = 'user__last_name'
    get_user_lastname.short_description = 'Last name'

class MailListAdmin(admin.ModelAdmin):
    search_fields = ['email', 'first_name', 'last_name']
    list_filter = ['email', 'first_name','last_name']
    list_display = ['email', 'first_name','last_name']

class FeedbackContactAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject','date']
    list_filter = ['date']
    search_fields = ['full_name', 'email']
    date_hierarchy = 'date'

class UploadAdmin(admin.ModelAdmin):
    search_fields = ['user__first_name', 'user__last_name', 'user__username']
    list_filter = ['date','user__username','user__first_name', 'user__last_name' ]
    list_display = ['user', 'get_user_firstname', 'get_user_lastname','date', 'to_user_status', 'get_status_date']

    def to_user_status(self, obj):
        link = reverse("admin:app_userstatus_change", args=[obj.user.userstatus.id])
        return format_html('<a href="{}">{}</a>', link, obj.user.userstatus.status)
    to_user_status.short_description = "User Status" 

    def get_status_date(self, obj):
        return obj.user.userstatus.modified
    get_status_date.short_description = "Modified"


    def get_user_firstname(self, obj):
        return obj.user.first_name
    get_user_firstname.admin_order_field  = 'user__first_name'
    get_user_firstname.short_description = 'First name'

    def get_user_lastname(self, obj):
        return obj.user.last_name
    get_user_lastname.admin_order_field  = 'user__last_name'
    get_user_lastname.short_description = 'Last name'

class LinksAdmin(admin.ModelAdmin):
    list_display = ['name', 'link']
    list_filter = ['name']
    search_fields = ['name']

class DownloadFormsAdmin(admin.ModelAdmin):
    list_display = ['group', 'date']

    
# Register your models here.
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(UserStatus,UserStatusAdmin)
admin.site.register(MailList,MailListAdmin)
admin.site.register(FeedbackContact,FeedbackContactAdmin)
admin.site.register(PoliceUpload, UploadAdmin)
admin.site.register(MemberUpload, UploadAdmin)
admin.site.register(Links,LinksAdmin)
admin.site.register(DownloadForms, DownloadFormsAdmin)