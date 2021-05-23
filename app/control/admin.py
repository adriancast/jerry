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
        'required_hours'
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
        'required_hours',
        'delta_roi',
        'delayed_tasks',
        'delayed_tasks_percentage',
        'is_cancelled',
    ]

    readonly_fields = [
        'delta_roi',
        'completed_tasks',
        'is_cancelled',
    ]

    list_filter = [
        'category',
        'priority',
        'is_cancelled',
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
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