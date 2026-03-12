from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'position_title', 'status', 'job_type', 'date_applied', 'user']
    list_filter = ['status', 'job_type', 'location_type']
    search_fields = ['company_name', 'position_title', 'user__username']
    date_hierarchy = 'date_applied'
