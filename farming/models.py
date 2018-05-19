# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import date 

class FarmerDetail(models.Model):
    name = models.CharField(max_length=30, blank=False)
    phone = models.CharField(max_length=30, blank=False)
    language = models.CharField(max_length=30, blank=False, null=False)
        
    def __str__(self):
        return str(self.id)
    
class FarmDetail(models.Model):
    farmer = models.ForeignKey(FarmerDetail, on_delete=models.CASCADE)
    area = models.FloatField(null=False, blank=False, default=0)
    village = models.CharField(max_length=20, blank=False)
    crop = models.CharField(max_length=20, blank=False)
    
    def __str__(self):
        return str(self.id)
    
class ScheduleDetail(models.Model):
    farm = models.ForeignKey(FarmDetail, on_delete=models.CASCADE)
    sowingdate = models.DateField(default=date.today)
    days = models.IntegerField(blank=False)
    fertiliser = models.CharField(max_length=20, blank=False)
    quantity = models.FloatField(blank=False)
    UNIT_CHOICES = (
        ("TON", 'ton'),
        ("KG", 'kilogram'),
        ("G", 'gram'),
        ("L", 'litre'),
        ("ML", 'mililitre'),
    )
    quantity_unit = models.CharField(max_length=3, choices=UNIT_CHOICES, blank=False)