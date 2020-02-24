from django.db import models

from .problem import Problem
from .test import Test

class TestSet(models.Model):
	testset_id = models.AutoField(primary_key=True)
	full_score = models.FloatField()

	problem = models.ForeignKey(
		Problem,
		models.CASCADE,
		related_name='+',
	)

	tests = models.ManyToManyField(Test, related_name='+', blank=True)

	class Meta:
		ordering = ['testset_id']
