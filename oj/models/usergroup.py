from django.db import models

from .user import User

class UserGroup(models.Model):
	gid = models.AutoField(primary_key=True)
	group_name = models.CharField(max_length=128)
	description = models.TextField(default='')

	users = models.ManyToManyField(User, related_name='usergroups', blank=True)

	class Meta:
		ordering = ['gid']
