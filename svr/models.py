from django.db import models

class SVRmodel(models.Model):
    share_addr = models.CharField(max_length=200)
    fund_addr = models.CharField(max_length=200)
    mse = models.CharField(max_length=200)
    mae = models.CharField(max_length=200)
# Create your models here.