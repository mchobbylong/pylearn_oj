from django.db import models
from datetime import datetime

from .problem import Problem
from .usergroup import UserGroup

class Task(models.Model):
	task_id = models.AutoField(primary_key=True)
	task_name = models.CharField(max_length=64)
	description = models.TextField(default='')
	deadline = models.DateTimeField()

	problems = models.ManyToManyField(
		Problem,
		related_name='tasks',
		blank=True,
	)

	usergroups = models.ManyToManyField(
		UserGroup,
		related_name='tasks',
		blank=True,
	)

	class Meta:
		ordering = ['task_id']

	def __str__(self):
		return self.task_name

	@property
	def available(self):
		return self.deadline > datetime.now()
