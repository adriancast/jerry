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

    @property
    def is_validated_by_manager(self):
        default = False
        has_general_manager_revision = bool(self.general_manager_revision)
        return (
            self.general_manager_revision.is_validated
            if has_general_manager_revision
            else default
        )

    def __str__(self):
        return self.name

class PortfolioConfigurationGeneralManagerRevision(models.Model):
    portfolio_configuration = models.ForeignKey(
        PortfolioConfiguration,
        on_delete=models.CASCADE,
        related_name='general_manager_revision'
    )

    is_validated = models.BooleanField(default=False)

    # total_budget_eur = models.PositiveIntegerField(blank=True, null=True)
    # dev_resources_hours = models.PositiveIntegerField(blank=True, null=True)
    # sysops_resources_hours = models.PositiveIntegerField(blank=True, null=True)
    # management_resources_hours = models.PositiveIntegerField(blank=True, null=True)
    # marketing_resources_hours = models.PositiveIntegerField(blank=True, null=True)
    # operative_resources_hours = models.PositiveIntegerField(blank=True, null=True)

    comment = models.TextField(blank=True, null=True)


class ProjectWallet(models.Model):
    portfolio_configuration = models.OneToOneField(
        PortfolioConfiguration,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    name = models.CharField(max_length=256)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()

    is_open = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    STATUS_PENDING = 'PENDING'
    STATUS_IN_PROGRESS = 'IN_PROGRESS'
    STATUS_BLOCKED = 'BLOCKED'
    STATUS_DONE = 'DONE'
    STATUS_CANCELLED = 'CANCELLED'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_IN_PROGRESS, 'In progress'),
        (STATUS_BLOCKED, 'Blocked'),
        (STATUS_DONE, 'Done'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    status = models.CharField(
        max_length=32,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )

    wallet = models.ForeignKey(
        ProjectWallet,
        on_delete=models.CASCADE,
    )
    priority = models.PositiveIntegerField(default=10)
    name = models.CharField(max_length=256)
    description = models.TextField()
    start_date = models.DateField()

    category = models.CharField(max_length=256, blank=True)

    estimated_roi = models.PositiveIntegerField()
    real_roi = models.IntegerField()

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
    total_real_cost = models.PositiveIntegerField(help_text='Money spent in the project in €')

    is_in_risk = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.delta_roi = round(self.real_roi / self.estimated_roi, 2)
        completed_milestones = len(self.milestones.filter(status=ProjectMilestone.STATUS_DONE))
        total_milestones = len(self.milestones.all())
        self.completed_tasks = completed_milestones / total_milestones
        self.delayed_tasks = len(
            self.milestones.filter(due_date__lt=date.today())
        )
        self.delayed_tasks_percentage = self.delayed_tasks / total_milestones

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

        self.is_in_risk = any([
            self.delayed_tasks_percentage > 0.25,
            self.estimated_total_cost < self.total_real_cost
        ])

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


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

    status = models.CharField(
        max_length=32,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    name = models.CharField(max_length=256)
    description = models.TextField()
    due_date = models.DateField()

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='milestones',
    )

    used_dev_resources_hours = models.PositiveIntegerField(help_text='Cost €/h: {}'.format(COST_DEV))
    used_sysops_resources_hours = models.PositiveIntegerField(help_text='Cost €/h: {}'.format(COST_SYSOPS))
    used_management_resources_hours = models.PositiveIntegerField(help_text='Cost €/h: {}'.format(COST_MANAGEMENT))
    used_marketing_resources_hours = models.PositiveIntegerField(help_text='Cost €/h: {}'.format(COST_MARKETING))
    used_operative_resources_hours = models.PositiveIntegerField(help_text='Cost €/h: {}'.format(COST_OPERATIVE))
    used_resources_cost = models.PositiveIntegerField(default=0)

    used_other_cost = models.PositiveIntegerField(help_text='Total costs in €')
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


class WalletReport(models.Model):

    total_tasks = models.PositiveIntegerField()
    total_delayed_tasks = models.PositiveIntegerField()
    total_delayed_tasks_percentage = models.FloatField()

    total_costs = models.PositiveIntegerField()
    total_revenue = models.PositiveIntegerField()

