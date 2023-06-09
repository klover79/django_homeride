from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile
from django.utils.html import format_html


class AccountAdmin(UserAdmin):
    list_display = ('id','email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active', )
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login','date_joined')
    ordering = ('-date_joined',)

    filter_horizontal=()
    list_filter=()
    fieldsets=()

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30", style="border-radius:50%;">'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'is_active',  'user', 'city', 'state', 'country', 'is_student', 'is_manager', 'is_org_admin', )


admin.site.register(User, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
