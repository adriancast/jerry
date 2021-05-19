from django.contrib import admin
from .models import PortfolioConfiguration, Project


class PortfolioConfigurationAdmin(admin.ModelAdmin):
    list_display = [
        'start_date',
        'end_date',
        'is_validated',
    ]
    pass

class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
        'start_date',
    ]

# Register your models here.
admin.site.register(Project, ProjectAdmin)
admin.site.register(PortfolioConfiguration, PortfolioConfigurationAdmin)