from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'position_title', 'user', 'status', 'priority', 'date_applied', 'updated_at']
    list_filter = ['status', 'job_type', 'location', 'priority']
    search_fields = ['company_name', 'position_title', 'user__username', 'notes']
    date_hierarchy = 'date_applied'
    ordering = ['-date_applied']
    readonly_fields = ['created_at', 'updated_at']
