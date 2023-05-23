from django.contrib import admin

from .models import Organisation, OrganisationManager, OrganisationClass, OrganisationPayment

class OrganisationManagerAdmin(admin.ModelAdmin):
    list_display = ('organisation', 'is_active',  'organisation_role', 'user', 'created_date', 'modified_date')
    list_display_links = ('organisation', 'is_active', 'organisation_role', 'user',)
    readonly_fields = ('created_date', 'modified_date')
    ordering = ('-created_date',)

    filter_horizontal=()
    list_filter=()
    fieldsets=()

class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('id','organisation_name', 'email_address', 'is_active' )
    list_display_links = ('organisation_name',)
    filter_horizontal=()
    list_filter=()
    fieldsets=()

class OrganisationClassAdmin(admin.ModelAdmin):
    list_display = ('organisation', 'grade', 'name', 'created_date', 'modified_date')

admin.site.register(Organisation,OrganisationAdmin)
admin.site.register(OrganisationManager, OrganisationManagerAdmin)
admin.site.register(OrganisationClass,OrganisationClassAdmin)