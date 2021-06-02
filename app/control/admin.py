from django.contrib import admin
from .models import (
    PortfolioConfiguration,
    Project,
    ProjectWallet,
    ProjectMilestone,
    PortfolioConfigurationGeneralManagerRevision
)

class ProjectWalletInline(admin.TabularInline):
    model = ProjectWallet
    extra = 0
    can_delete = False
    show_change_link = True
    readonly_fields = [
        'name',
        'start_date',
        'end_date',
        'description',
    ]
    def has_add_permission(self, request, obj=None):
        return False


    def has_delete_permission(self, request, obj=None):
        return False

class PortfolioConfigurationGeneralManagerRevisionInline(admin.TabularInline):
    model = PortfolioConfigurationGeneralManagerRevision
    extra = 0
    show_change_link = True
    can_delete = False
    readonly_fields = [
        'comment',
        'is_validated'
    ]
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class PortfolioConfigurationGeneralManagerRevisionAdmin(admin.ModelAdmin):
    list_display = [
        'portfolio_configuration',
        'comment',
        'is_validated',
    ]

class PortfolioConfigurationAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'start_date',
        'end_date',
        'total_budget_eur'
    ]

    readonly_fields = [
        'total_hours',
        'total_budget_resources',
        'total_budget_eur',
    ]

    inlines = [
        PortfolioConfigurationGeneralManagerRevisionInline,
        ProjectWalletInline,
    ]

class ProjectInline(admin.TabularInline):
    model = Project
    can_delete = False
    extra = 0
    show_change_link = True
    readonly_fields = [
        'priority',
        'name',
        'description',
        'start_date',
        'is_cancelled',
        'delayed_tasks_percentage',
        'delayed_tasks',
        'completed_tasks',
        'delta_roi',
        'real_roi',
        'estimated_roi',
        'category',
        'status',
        'dev_resources_hours',
        'sysops_resources_hours',
        'management_resources_hours',
        'marketing_resources_hours',
        'operative_resources_hours',
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class ProjectWalletAdmin(admin.ModelAdmin):
    list_display = [
        'start_date',
        'end_date',
        'description',
    ]
    inlines = [
        ProjectInline,
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['portfolio_configuration'].queryset = PortfolioConfiguration.objects.filter(
            general_manager_revision__is_validated=True
        )
        return form


class ProjectMilestoneAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'due_date',
        'status',
    ]
    search_fields = [
        'name',
    ]
    list_filter = [
        'status'
    ]

class ProjectMilestoneInline(admin.TabularInline):
    model = ProjectMilestone
    show_change_link = True
    extra = 0
    can_delete = False


class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        ProjectMilestoneInline,
    ]
    list_display = [
        'name',
        'description',
        'start_date',
        'priority',
        'category',
        'delta_roi',
        'delayed_tasks',
        'delayed_tasks_percentage',
        'is_cancelled',
    ]

    readonly_fields = [
        'delta_roi',
        'completed_tasks',
        'is_cancelled',
        'delayed_tasks',
        'delayed_tasks_percentage',
        'estimated_resources_cost',
        'estimated_total_cost',
        'estimated_total_hours',
        'estimated_total_hours',
        'is_in_risk',
    ]

    list_filter = [
        'category',
        'priority',
        'is_cancelled',
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not hasattr(obj, 'wallet'):
            form.base_fields['wallet'].queryset = ProjectWallet.objects.filter(
                is_open=True
            )
        return form

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields

# Register your models here.
admin.site.register(Project, ProjectAdmin)
admin.site.register(PortfolioConfiguration, PortfolioConfigurationAdmin)
admin.site.register(ProjectMilestone, ProjectMilestoneAdmin)
admin.site.register(ProjectWallet, ProjectWalletAdmin)
admin.site.register(PortfolioConfigurationGeneralManagerRevision, PortfolioConfigurationGeneralManagerRevisionAdmin)