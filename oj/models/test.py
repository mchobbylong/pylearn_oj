from django.db import models

class Test(models.Model):
	test_id = models.AutoField(primary_key=True)
	score = models.FloatField()
	code = models.TextField()

	class Meta:
		ordering = ['test_id']
