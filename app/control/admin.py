from django.contrib import admin
from .models import (
    PortfolioConfiguration,
    Project,
    ProjectWallet,
    ProjectMilestone,
    PortfolioConfigurationGeneralManagerRevision,
    ProjectRevision,
    ProjectWalletRevision,
    ProjectWalletBlockedNewProjectsRevision,
    ProjectWalletIsClosedRevision,
)

class ProjectWalletInline(admin.TabularInline):
    model = ProjectWallet
    extra = 0
    can_delete = False
    show_change_link = True
    show_change_link = True
    readonly_fields = [
        'name',
        'start_date',
        'end_date',
        'description',
        'is_open',
        'can_add_new_projects',
        'related_data_can_be_edited',
        'projects_total_estimated_costs',
        'not_assigned_total_costs',
        'projects_dev_resources_hours',
        'not_assigned_dev_resources_hours',
        'projects_sysops_resources_hours',
        'not_assigned_sysops_resources_hours',
        'projects_management_resources_hours',
        'not_assigned_management_resources_hours',
        'projects_marketing_resources_hours',
        'not_assigned_marketing_resources_hours',
        'projects_operative_resources_hours',
        'not_assigned_operative_resources_hours',
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

    def get_readonly_fields(self, request, obj=None, **kwargs):
        readonly_fields = []
        if obj and obj.is_validated:
            readonly_fields = [
                'portfolio_configuration',
                'comment',
                'is_validated',
            ]
        return readonly_fields


class ProjectRevisionInline(admin.TabularInline):
    model = ProjectRevision
    extra = 0
    show_change_link = True
    can_delete = False
    readonly_fields = [
        'comment',
        'is_validated',
        'score',
    ]
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class ProjectRevisionAdmin(admin.ModelAdmin):
    list_display = [
        'project',
        'comment',
        'is_validated',
        'score',
    ]

    def get_readonly_fields(self, request, obj=None, **kwargs):
        readonly_fields = []
        if obj and obj.is_validated:
            readonly_fields = [
                'project',
                'comment',
                'is_validated',
                'score',
            ]
        return readonly_fields

class ProjectWalletRevisionInline(admin.TabularInline):
    model = ProjectWalletRevision
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

class ProjectWalletRevisionAdmin(admin.ModelAdmin):
    list_display = [
        'project_wallet',
        'comment',
        'is_validated',
    ]

    def get_readonly_fields(self, request, obj=None, **kwargs):
        readonly_fields = []
        if obj and obj.is_validated:
            readonly_fields = [
                'project_wallet',
                'comment',
                'is_validated',
            ]
        return readonly_fields


class ProjectWalletIsClosedRevisionInline(admin.TabularInline):
    model = ProjectWalletIsClosedRevision
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


class ProjectWalletIsClosedRevisionAdmin(admin.ModelAdmin):
    list_display = [
        'project_wallet',
        'comment',
        'is_validated',
    ]

    def get_readonly_fields(self, request, obj=None, **kwargs):
        readonly_fields = []
        if obj and obj.is_validated:
            readonly_fields = [
                'project_wallet',
                'comment',
                'is_validated',
            ]
        return readonly_fields


class ProjectWalletBlockedNewProjectsRevisionInline(admin.TabularInline):
    model = ProjectWalletBlockedNewProjectsRevision
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

class ProjectWalletBlockedNewProjectsRevisionAdmin(admin.ModelAdmin):
    list_display = [
        'project_wallet',
        'comment',
        'is_validated',
    ]

    def get_readonly_fields(self, request, obj=None, **kwargs):
        readonly_fields = []
        if obj and obj.is_validated:
            readonly_fields = [
                'project_wallet',
                'comment',
                'is_validated',
            ]
        return readonly_fields

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

    def get_readonly_fields(self, request, obj=None, **kwargs):
        readonly_fields = [
            'total_hours',
            'total_budget_resources',
            'total_budget_eur',
        ]
        if obj and obj.is_validated_by_manager():
            readonly_fields = [
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
        return readonly_fields

class ProjectInline(admin.TabularInline):
    model = Project
    can_delete = False
    extra = 0
    show_change_link = True
    exclude = [
        'description',
        'start_date',
        'end_date',
        'is_cancelled',
        'delayed_tasks_percentage',
        'delayed_tasks',
        'completed_tasks',
        'delta_roi',
        'real_roi',
        'estimated_roi',
        'category',
        'estimated_dev_resources_hours',
        'estimated_sysops_resources_hours',
        'estimated_management_resources_hours',
        'estimated_marketing_resources_hours',
        'estimated_operative_resources_hours',
        'estimated_other_costs',
        'estimated_total_hours',
        'estimated_total_cost',
        'estimated_resources_cost',
        'estimated_other_cost',
        'total_real_cost',
        'is_in_risk',
        'is_in_risk_msg',
        'is_cancelled_msg',
    ]

    def get_readonly_fields(self, request, obj=None, **kwargs):
        readonly_fields = [
            'name'
        ]
        if obj and not obj.related_data_can_be_edited:
            readonly_fields += [
                'status',
                'priority',
            ]

        return readonly_fields

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class ProjectWalletAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'start_date',
        'end_date',
        'description',
    ]
    inlines = [
        ProjectInline,
        ProjectWalletRevisionInline,
        ProjectWalletBlockedNewProjectsRevisionInline,
        ProjectWalletIsClosedRevisionInline,
    ]

    readonly_fields = [
        'projects_total_estimated_costs',
        'not_assigned_total_costs',
        'projects_dev_resources_hours',
        'not_assigned_dev_resources_hours',
        'projects_sysops_resources_hours',
        'not_assigned_sysops_resources_hours',
        'projects_management_resources_hours',
        'not_assigned_management_resources_hours',
        'projects_marketing_resources_hours',
        'not_assigned_marketing_resources_hours',
        'projects_operative_resources_hours',
        'not_assigned_operative_resources_hours',
        'is_open',
        'can_add_new_projects',
        'related_data_can_be_edited',
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


    def get_readonly_fields(self, request, obj=None, **kwargs):
        readonly_fields = [
            'total_real_cost',
        ]
        if obj and obj.project.wallet and not obj.project.wallet.related_data_can_be_edited:
            readonly_fields += [
                'project',
                'status',
                'name',
                'description',
                'due_date',
                'used_dev_resources_hours',
                'used_sysops_resources_hours',
                'used_management_resources_hours',
                'used_marketing_resources_hours',
                'used_operative_resources_hours',
                'used_resources_cost',
                'used_other_cost',
            ]
        return readonly_fields

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
        ProjectRevisionInline,
    ]
    exclude = [
        'is_in_risk',
        'is_cancelled',
    ]

    list_display = [
        'name',
        'status',
        'get_project_wallet',
        'description',
        'start_date',
        'end_date',
        'priority',
        'category',
        'delayed_tasks',
        'delayed_tasks_percentage',
        'is_cancelled_msg',
        'is_in_risk_msg',
    ]

    list_filter = [
        'category',
        'priority',
        'is_cancelled_msg',
        'is_in_risk_msg',
        'status',
    ]

    def get_project_wallet(self, obj):
        return str(obj.wallet)

    get_project_wallet.short_description = 'Project Wallet'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not hasattr(obj, 'wallet'):
            form.base_fields['wallet'].queryset = ProjectWallet.objects.filter(
                can_add_new_projects=True
            )
        return form

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = [
            'delta_roi',
            'completed_tasks',
            'delayed_tasks',
            'delayed_tasks_percentage',
            'estimated_resources_cost',
            'estimated_total_cost',
            'estimated_total_hours',
            'estimated_total_hours',
            'total_real_cost',
            'is_in_risk_msg',
            'is_cancelled_msg',
        ]
        if obj and not obj.wallet.can_add_new_projects:
            readonly_fields += [
                'estimated_roi',
                'estimated_dev_resources_hours',
                'estimated_sysops_resources_hours',
                'estimated_management_resources_hours',
                'estimated_marketing_resources_hours',
                'estimated_operative_resources_hours',
                'estimated_other_cost',
            ]
        if obj and obj.wallet and not obj.wallet.related_data_can_be_edited:
            readonly_fields += [
                'status',
                'wallet',
                'priority',
                'name',
                'description',
                'start_date',
                'end_date',
                'category',
                'real_roi',
            ]

        return readonly_fields

# Register your models here.
admin.site.register(Project, ProjectAdmin)
admin.site.register(PortfolioConfiguration, PortfolioConfigurationAdmin)
admin.site.register(ProjectMilestone, ProjectMilestoneAdmin)
admin.site.register(ProjectWallet, ProjectWalletAdmin)
admin.site.register(ProjectWalletRevision, ProjectWalletRevisionAdmin)
admin.site.register(PortfolioConfigurationGeneralManagerRevision, PortfolioConfigurationGeneralManagerRevisionAdmin)
admin.site.register(ProjectRevision, ProjectRevisionAdmin)
admin.site.register(ProjectWalletBlockedNewProjectsRevision, ProjectWalletBlockedNewProjectsRevisionAdmin)
admin.site.register(ProjectWalletIsClosedRevision, ProjectWalletIsClosedRevisionAdmin)