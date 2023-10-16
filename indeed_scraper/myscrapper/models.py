# scraper/models.py

# from django.db import models
from djongo import models

class Job(models.Model):
    title = models.CharField(max_length=255)
    href = models.URLField()
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    date = models.CharField(max_length=50)
    href_full = models.URLField()
    salary = models.CharField(max_length=255, null=True, blank=True)
