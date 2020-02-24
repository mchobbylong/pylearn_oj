from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from versatileimagefield.fields import VersatileImageField
from versatileimagefield.placeholder import OnStoragePlaceholderImage
import os

class User(AbstractUser):
	avatar = VersatileImageField(
		upload_to='avatars',
		blank=True,
		placeholder_image=OnStoragePlaceholderImage(path='default_avatar.jpg'),
	)
	item_per_page = models.IntegerField(default=20)

	class Meta:
		ordering = ['id']

	def __str__(self):
		return self.username
