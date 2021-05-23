from django.db import models
from datetime import datetime, date

class PortfolioConfiguration(models.Model):
    name = models.CharField(max_length=256)
    start_date = models.DateField()
    end_date = models.DateField()

    total_budget_eur = models.PositiveIntegerField()
    dev_resources_hours = models.PositiveIntegerField()
    sysops_resources_hours = models.PositiveIntegerField()
    management_resources_hours = models.PositiveIntegerField()
    marketing_resources_hours = models.PositiveIntegerField()
    operative_resources_hours = models.PositiveIntegerField()

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

    required_hours = models.PositiveIntegerField()

    category = models.CharField(max_length=256, blank=True)

    estimated_roi = models.PositiveIntegerField()
    real_roi = models.IntegerField()

    is_cancelled = models.BooleanField(default=False)

    # Internal fields
    delta_roi = models.FloatField(blank=True, null=True)
    completed_tasks = models.FloatField(blank=True, null=True)
    delayed_tasks = models.IntegerField(blank=True, null=True)
    delayed_tasks_percentage = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.delta_roi = round(self.real_roi / self.estimated_roi, 2)
        completed_milestones = len(self.milestones.filter(status=ProjectMilestone.STATUS_DONE))
        total_milestones = len(self.milestones.all())
        self.completed_tasks = completed_milestones / total_milestones
        self.delayed_tasks = len(
            self.milestones.filter(due_date__lt=date.today())
        )
        self.delayed_tasks_percentage = self.delayed_tasks / total_milestones

        self.is_cancelled = False
        if self.status == self.STATUS_CANCELLED:
            self.is_cancelled = True

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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.project.save()

    def __str__(self):
        return self.name
