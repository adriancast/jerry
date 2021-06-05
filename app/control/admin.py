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

    def get_form(self, request, obj=None, **kwargs):
        if obj and obj.is_validated:
            self.readonly_fields = [
                'portfolio_configuration',
                'comment',
                'is_validated',
            ]
        form = super().get_form(request, obj, **kwargs)
        return form

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

    def get_form(self, request, obj=None, **kwargs):
        if obj and obj.is_validated_by_manager():
            self.readonly_fields = [
                'start_date',
                'end_date',
                'name',
                'dev_resources_hours',
                'sysops_resources_hours',
                'management_resources_hours',
                'marketing_resources_hours',
                'operative_resources_hours',
                'other_costs_budget',
                'total_hours',
                'total_budget_resources',
                'total_budget_eur',
            ]
        form = super().get_form(request, obj, **kwargs)
        return form

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
        'estimated_dev_resources_hours',
        'estimated_sysops_resources_hours',
        'estimated_management_resources_hours',
        'estimated_marketing_resources_hours',
        'estimated_operative_resources_hours',
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

    exclude = [
        'used_resources_cost',
    ]

    readonly_fields = [
        'total_real_cost',
    ]

class ProjectMilestoneInline(admin.TabularInline):
    model = ProjectMilestone
    show_change_link = True
    extra = 0
    can_delete = False
    max_num = 0

    readonly_fields = [
        'name', 'status', 'description'
    ]

    exclude = [
        'due_date',
        'used_dev_resources_hours',
        'used_sysops_resources_hours',
        'used_management_resources_hours',
        'used_marketing_resources_hours',
        'used_operative_resources_hours',
        'used_resources_cost',
        'used_other_cost',
        'total_real_cost',
    ]


class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        ProjectMilestoneInline,
    ]
    exclude = [
        'is_in_risk',
        'is_cancelled',
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
        'is_cancelled_msg',
        'is_in_risk_msg',
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
        'is_in_risk_msg',
        'total_real_cost',
        'is_cancelled_msg',
    ]

    list_filter = [
        'category',
        'priority',
        'is_cancelled_msg',
        'is_in_risk_msg',
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