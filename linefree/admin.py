

from django.contrib import admin
from .models import Service, Organization, UserToken

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "start_time", "end_time")

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "org_type", "get_services_count")
    
    def get_services_count(self, obj):
        return obj.services.count()
    get_services_count.short_description = 'Services Count'

@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = ("token_number", "user", "service_type", "organization", "status", "created_at")
    list_filter = ("status", "service_type", "organization")