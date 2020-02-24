from django.db import models

from .user import User

class Announcement(models.Model):
	aid = models.AutoField(primary_key=True)
	title = models.CharField(max_length=64)
	description = models.TextField()
	publish_time = models.DateTimeField(auto_now_add=True)

	user = models.ForeignKey(
		User,
		models.SET_NULL,
		null=True,
		blank=True,
	)

	class Meta:
		ordering = ['-aid']

	def __str__(self):
		return self.title
