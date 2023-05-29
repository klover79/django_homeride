from django.contrib import admin
from .models import Dependent

class DependentAdmin(admin.ModelAdmin):
    list_display = ('identity','user', 'parent','organisation','organisation_class',)
    list_display_links =('parent','user',)
    filter_horizontal=()
    list_filter=('parent','organisation',)
    fieldsets=()
    search_fields = ['identity',]


admin.site.register(Dependent,DependentAdmin)

