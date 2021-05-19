from django.db import models

class PortfolioConfiguration(models.Model):
    name = models.CharField(max_length=256)
    start_date = models.DateField()
    end_date = models.DateField()
    is_validated = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class ProjectWallet(models.Model):
    portfolio_configuration = models.ForeignKey(
        PortfolioConfiguration,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=256)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    is_validated = models.BooleanField(default=False)

    def __str__(self):
        return self.name



class Project(models.Model):
    wallet = models.ForeignKey(
        ProjectWallet,
        on_delete=models.CASCADE,
    )
    priority = models.PositiveIntegerField(default=10)
    name = models.CharField(max_length=256)
    description = models.TextField()
    start_date = models.DateField()

    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ProjectMilestone(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    due_date = models.DateField()

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
