from django.db import models

from .user import User
from .problem import Problem
from .testset import TestSet
from .task import Task

from datetime import datetime

class Submission(models.Model):
	sid = models.AutoField(primary_key=True)
	result = models.TextField(default='')
	score = models.FloatField(null=True)
	full_score = models.FloatField(null=True)
	code = models.TextField()
	is_solution = models.BooleanField(default=False)
	submit_time = models.DateTimeField(auto_now_add=True)

	problem = models.ForeignKey(
		Problem,
		models.CASCADE,
		related_name='submissions',
	)

	testset = models.ForeignKey(
		TestSet,
		models.PROTECT,
		null=True,
		related_name='+',
	)

	user = models.ForeignKey(
		User,
		models.CASCADE,
		related_name='submissions',
	)

	tasks = models.ManyToManyField(
		Task,
		related_name='submissions',
		blank=True,
	)

	class Meta:
		ordering = ['-sid']

	def __str__(self):
		return self.sid

	def status(self, request):
		if not request.user.is_superuser:
			if self.tasks.filter(deadline__gt=datetime.now()).exists():
				return 'hidden'
		if not self.result:
			return 'pending'
		if self.result == 'running':
			return 'running'
		if self.result == 'system_error':
			return 'system_error'
		if self.full_score == self.score:
			return 'accepted'
		if self.full_score > self.score:
			return 'wrong_answer'
		return 'other'
