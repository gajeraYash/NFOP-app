from django.contrib import admin
from app.models import *

# Modify your admin layout here.
class UserStatusAdmin(admin.ModelAdmin):
    search_fields = ['user__first_name', 'user__last_name', 'user__username']
    list_filter = ['status','user__username','user__first_name', 'user__last_name' ]
    list_display = ['user', 'get_user_firstname', 'get_user_lastname','status' ]
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
    search_fields = ['user__first_name', 'user__last_name', 'user__username', 'phone_number' 'address_1', 'city', 'state', 'zip_code']
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

class LinksAdmin(admin.ModelAdmin):
    list_display = ['name', 'link']
    list_filter = ['name']
    search_fields = ['name']
    
# Register your models here.
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(UserStatus,UserStatusAdmin)
admin.site.register(MailList,MailListAdmin)
admin.site.register(FeedbackContact,FeedbackContactAdmin)
admin.site.register(Links,LinksAdmin)
