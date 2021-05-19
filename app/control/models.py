from django.db import models

class PortfolioConfiguration(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    is_validated = models.BooleanField(default=False)


class Project(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    start_date = models.DateField()