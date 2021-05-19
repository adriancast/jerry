from django.contrib import admin
from .models import (
    PortfolioConfiguration,
    Project,
    ProjectWallet,
    ProjectMilestone
)

class PortfolioConfigurationAdmin(admin.ModelAdmin):
    list_display = [
        'start_date',
        'end_date',
        'is_validated',
    ]

class ProjectWalletAdmin(admin.ModelAdmin):
    list_display = [
        'start_date',
        'end_date',
        'description',
        'is_validated',
    ]

class ProjectMilestoneAdmin(admin.ModelAdmin):
    list_display = [
        'description',
        'due_date',
    ]

class ProjectMilestoneInline(admin.TabularInline):
    model = ProjectMilestone


class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        ProjectMilestoneInline,
    ]
    list_display = [
        'name',
        'description',
        'start_date',
        'priority',
    ]

# Register your models here.
admin.site.register(Project, ProjectAdmin)
admin.site.register(PortfolioConfiguration, PortfolioConfigurationAdmin)
admin.site.register(ProjectMilestone, ProjectMilestoneAdmin)
admin.site.register(ProjectWallet, ProjectWalletAdmin)