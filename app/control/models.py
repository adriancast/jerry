from django.db import models
from datetime import datetime, date

# Costs for every hour of each resource in EUR
COST_DEV = 30
COST_SYSOPS = 30
COST_MANAGEMENT = 40
COST_MARKETING = 35
COST_OPERATIVE = 25


class PortfolioConfiguration(models.Model):
    name = models.CharField(max_length=256)
    start_date = models.DateField()
    end_date = models.DateField()

    dev_resources_hours = models.PositiveIntegerField(help_text='Cost €/h: {}'.format(COST_DEV))
    sysops_resources_hours = models.PositiveIntegerField(help_text='Cost €/h: {}'.format(COST_SYSOPS))
    management_resources_hours = models.PositiveIntegerField(help_text='Cost €/h: {}'.format(COST_MANAGEMENT))
    marketing_resources_hours = models.PositiveIntegerField(help_text='Cost €/h: {}'.format(COST_MARKETING))
    operative_resources_hours = models.PositiveIntegerField(help_text='Cost €/h: {}'.format(COST_OPERATIVE))

    other_costs_budget = models.PositiveIntegerField()

    # Internal fields
    total_hours = models.PositiveIntegerField()
    total_budget_resources = models.PositiveIntegerField()
    total_budget_eur = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        self.total_hours = sum(
            [
                self.dev_resources_hours,
                self.sysops_resources_hours,
                self.management_resources_hours,
                self.marketing_resources_hours,
                self.operative_resources_hours,
            ]
        )

        self.total_budget_resources = sum(
            [
                self.dev_resources_hours * COST_DEV,
                self.sysops_resources_hours * COST_SYSOPS,
                self.management_resources_hours * COST_MANAGEMENT,
                self.marketing_resources_hours * COST_MARKETING,
                self.operative_resources_hours * COST_OPERATIVE,
            ]
        )

        self.total_budget_eur = self.other_costs_budget + self.total_budget_resources

        super().save(*args, **kwargs)

    def is_validated_by_manager(self):
        default = False
        has_general_manager_revision = hasattr(self, 'general_manager_revision')
        return (
            self.general_manager_revision.is_validated
            if has_general_manager_revision
            else default
        )

    def __str__(self):
        return self.name

class PortfolioConfigurationGeneralManagerRevision(models.Model):
    portfolio_configuration = models.OneToOneField(
        PortfolioConfiguration,
        on_delete=models.CASCADE,
        related_name='general_manager_revision'
    )

    is_validated = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)


class ProjectWallet(models.Model):
    portfolio_configuration = models.ForeignKey(
        PortfolioConfiguration,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=256)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()

    is_open = models.BooleanField(default=True)
    can_add_new_projects = models.BooleanField(default=True)

    # Internal fields
    projects_total_estimated_costs = models.IntegerField(default=0)
    not_assigned_total_costs = models.IntegerField(default=0)

    projects_dev_resources_hours = models.IntegerField(default=0)
    not_assigned_dev_resources_hours = models.IntegerField(default=0)

    projects_sysops_resources_hours = models.IntegerField(default=0)
    not_assigned_sysops_resources_hours = models.IntegerField(default=0)

    projects_management_resources_hours = models.IntegerField(default=0)
    not_assigned_management_resources_hours = models.IntegerField(default=0)

    projects_marketing_resources_hours = models.IntegerField(default=0)
    not_assigned_marketing_resources_hours = models.IntegerField(default=0)

    projects_operative_resources_hours = models.IntegerField(default=0)
    not_assigned_operative_resources_hours = models.IntegerField(default=0)


    def calculate_relation_data(self):
        self.projects_total_estimated_costs = 0
        self.not_assigned_total_costs = 0

        self.not_assigned_dev_resources_hours = 0
        self.projects_dev_resources_hours = 0

        self.projects_sysops_resources_hours = 0
        self.not_assigned_sysops_resources_hours = 0

        self.projects_management_resources_hours = 0
        self.not_assigned_management_resources_hours = 0

        self.projects_marketing_resources_hours = 0
        self.not_assigned_marketing_resources_hours = 0

        self.projects_operative_resources_hours = 0
        self.not_assigned_operative_resources_hours = 0

        # Pinxo I cant do this properly using the queryset queries
        filtered_projects = [
            p for p in self.projects.all() if p.status != Project.STATUS_NOT_ACCEPTED
        ]


        for project in filtered_projects:
            self.projects_total_estimated_costs += project.estimated_total_cost
            self.not_assigned_total_costs = self.portfolio_configuration.total_budget_eur - self.projects_total_estimated_costs

            self.projects_dev_resources_hours += project.estimated_dev_resources_hours
            self.not_assigned_dev_resources_hours = self.portfolio_configuration.dev_resources_hours - self.projects_dev_resources_hours

            self.projects_sysops_resources_hours += project.estimated_sysops_resources_hours
            self.not_assigned_sysops_resources_hours = self.portfolio_configuration.sysops_resources_hours - self.projects_sysops_resources_hours

            self.projects_management_resources_hours += project.estimated_management_resources_hours
            self.not_assigned_management_resources_hours = self.portfolio_configuration.management_resources_hours - self.projects_management_resources_hours

            self.projects_marketing_resources_hours += project.estimated_marketing_resources_hours
            self.not_assigned_marketing_resources_hours = self.portfolio_configuration.marketing_resources_hours - self.projects_marketing_resources_hours

            self.projects_operative_resources_hours += project.estimated_operative_resources_hours
            self.not_assigned_operative_resources_hours = self.portfolio_configuration.operative_resources_hours - self.projects_operative_resources_hours


    def save(self, *args, **kwargs):
        self.calculate_relation_data()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProjectWalletBlockedNewProjectsRevision(models.Model):
    project_wallet = models.OneToOneField(
        ProjectWallet,
        on_delete=models.CASCADE,
        related_name='blocked_new_projects_revision'
    )
    is_validated = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.project_wallet.can_add_new_projects = not self.is_validated
        self.project_wallet.save()
        super().save(*args, **kwargs)


class ProjectWalletRevision(models.Model):
    project_wallet = models.OneToOneField(
        ProjectWallet,
        on_delete=models.CASCADE,
        related_name='general_manager_revision'
    )
    is_validated = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)

class Project(models.Model):
    STATUS_PENDING = 'PENDING'
    STATUS_IN_PROGRESS = 'IN_PROGRESS'
    STATUS_BLOCKED = 'BLOCKED'
    STATUS_DONE = 'DONE'
    STATUS_CANCELLED = 'CANCELLED'
    STATUS_NOT_ACCEPTED = 'NOT_ACCEPTED'
    STATUS_ACCEPTED = 'ACCEPTED'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_IN_PROGRESS, 'In progress'),
        (STATUS_BLOCKED, 'Blocked'),
        (STATUS_DONE, 'Done'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_NOT_ACCEPTED, 'Not accepted'),
        (STATUS_ACCEPTED, 'Accepted'),
    ]

    status = models.CharField(
        max_length=32,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )

    wallet = models.ForeignKey(
        ProjectWallet,
        on_delete=models.CASCADE,
        related_name='projects',
    )
    priority = models.PositiveIntegerField(default=10)
    name = models.CharField(max_length=256)
    description = models.TextField()
    start_date = models.DateField()

    category = models.CharField(max_length=256, blank=True)

    estimated_roi = models.PositiveIntegerField()
    real_roi = models.IntegerField(default=0)

    is_cancelled = models.BooleanField(default=False)

    estimated_dev_resources_hours = models.PositiveIntegerField(help_text='Cost €/h: {}'.format(COST_DEV))
    estimated_sysops_resources_hours = models.PositiveIntegerField(help_text='Cost €/h: {}'.format(COST_SYSOPS))
    estimated_management_resources_hours = models.PositiveIntegerField(help_text='Cost €/h: {}'.format(COST_MANAGEMENT))
    estimated_marketing_resources_hours = models.PositiveIntegerField(help_text='Cost €/h: {}'.format(COST_MARKETING))
    estimated_operative_resources_hours = models.PositiveIntegerField(help_text='Cost €/h: {}'.format(COST_OPERATIVE))
    estimated_other_cost = models.PositiveIntegerField(help_text='Total costs in €')

    # Internal fields
    delta_roi = models.FloatField(blank=True, null=True)
    completed_tasks = models.FloatField(blank=True, null=True)
    delayed_tasks = models.IntegerField(blank=True, null=True)
    delayed_tasks_percentage = models.FloatField(blank=True, null=True)
    estimated_total_hours = models.PositiveIntegerField(help_text='€')
    estimated_total_cost = models.PositiveIntegerField(help_text='€')
    estimated_resources_cost = models.PositiveIntegerField(help_text='€')
    total_real_cost = models.PositiveIntegerField(help_text='Money spent in the project in €', default=0)

    is_in_risk = models.BooleanField(default=False)
    is_in_risk_msg = models.CharField(default='', max_length=256)
    is_cancelled_msg = models.CharField(default='', max_length=256)

    def save(self, *args, **kwargs):
        self.delta_roi = round(self.real_roi / self.estimated_roi, 2)
        completed_milestones = len(self.milestones.filter(status=ProjectMilestone.STATUS_DONE))
        total_milestones = len(self.milestones.all())
        self.completed_tasks = (
            completed_milestones / total_milestones
        ) if total_milestones else 0
        self.delayed_tasks = len(
            self.milestones.filter(due_date__lt=date.today())
        )
        self.delayed_tasks_percentage = (
            self.delayed_tasks / total_milestones
        ) if total_milestones else 0

        self.estimated_total_hours = sum(
            [
                self.estimated_dev_resources_hours,
                self.estimated_sysops_resources_hours,
                self.estimated_management_resources_hours,
                self.estimated_marketing_resources_hours,
                self.estimated_operative_resources_hours,
            ]
        )

        self.estimated_resources_cost = sum(
            [
                self.estimated_dev_resources_hours * COST_DEV,
                self.estimated_sysops_resources_hours * COST_SYSOPS,
                self.estimated_management_resources_hours * COST_MANAGEMENT,
                self.estimated_marketing_resources_hours * COST_MARKETING,
                self.estimated_operative_resources_hours * COST_OPERATIVE,
            ]
        )

        self.estimated_total_cost = self.estimated_resources_cost + self.estimated_other_cost

        self.is_cancelled = False
        if self.status == self.STATUS_CANCELLED:
            self.is_cancelled = True

        delayed_tasks_percentage_in_risk = (
            self.delayed_tasks_percentage > 0.25
        )
        self.is_cancelled_msg = (
            'PROJECT CANCELLED' if self.is_cancelled else 'PROJECT NOT CANCELLED'
        )


        self.is_in_risk_msg = '✅ The project is not in risk'
        if delayed_tasks_percentage_in_risk:
            self.is_in_risk_msg = '🔥 There is a more than a 25% of delay in tasks'

        estimated_total_cost_in_risk = (
            self.estimated_total_cost < self.total_real_cost
        )

        if estimated_total_cost_in_risk:
            self.is_in_risk_msg = '🔥 Real costs are higher than the estimated costs'

        self.is_in_risk = any([
            delayed_tasks_percentage_in_risk,
            estimated_total_cost_in_risk
        ])

        self.total_real_cost = sum([
            m.total_real_cost for m in self.milestones.all()
        ])

        super().save(*args, **kwargs)
        self.wallet.save()



    def __str__(self):
        return self.name


class ProjectRevision(models.Model):
    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        related_name='cio_revision'
    )

    is_validated = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)


class ProjectMilestone(models.Model):
    STATUS_PENDING = 'PENDING'
    STATUS_IN_PROGRESS = 'IN_PROGRESS'
    STATUS_BLOCKED = 'BLOCKED'
    STATUS_DONE = 'DONE'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_IN_PROGRESS, 'In progress'),
        (STATUS_BLOCKED, 'Blocked'),
        (STATUS_DONE, 'Done'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='milestones',
    )

    status = models.CharField(
        max_length=32,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    name = models.CharField(max_length=256)
    description = models.TextField()
    due_date = models.DateField()

    used_dev_resources_hours = models.PositiveIntegerField(default=0, help_text='Cost €/h: {}'.format(COST_DEV))
    used_sysops_resources_hours = models.PositiveIntegerField(default=0, help_text='Cost €/h: {}'.format(COST_SYSOPS))
    used_management_resources_hours = models.PositiveIntegerField(default=0, help_text='Cost €/h: {}'.format(COST_MANAGEMENT))
    used_marketing_resources_hours = models.PositiveIntegerField(default=0, help_text='Cost €/h: {}'.format(COST_MARKETING))
    used_operative_resources_hours = models.PositiveIntegerField(default=0, help_text='Cost €/h: {}'.format(COST_OPERATIVE))
    used_resources_cost = models.PositiveIntegerField(default=0)

    used_other_cost = models.PositiveIntegerField(default=0, help_text='Total costs in €')
    total_real_cost = models.PositiveIntegerField(help_text='Money spent in this task in €')

    def save(self, *args, **kwargs):
        self.used_resources_cost = sum(
            [
                self.used_dev_resources_hours * COST_DEV,
                self.used_sysops_resources_hours * COST_SYSOPS,
                self.used_management_resources_hours * COST_MANAGEMENT,
                self.used_marketing_resources_hours * COST_MARKETING,
                self.used_operative_resources_hours * COST_OPERATIVE,
            ]
        )

        self.total_real_cost = self.used_resources_cost + self.used_other_cost

        super().save(*args, **kwargs)
        self.project.save()

    def __str__(self):
        return self.name
