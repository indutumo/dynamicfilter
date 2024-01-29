from django.db import models
from django.utils import timezone
from datetime import datetime

class Population(models.Model):
	name = models.CharField(max_length=100)
	code = models.CharField(max_length=5)
	year = models.CharField(max_length=5)
	value = models.DecimalField(default=0.00,max_digits=1000,decimal_places=2)

	def __str__(self):
		return self.name
