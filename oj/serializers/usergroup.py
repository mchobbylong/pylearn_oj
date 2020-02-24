from rest_framework import serializers
from oj.models import UserGroup
from .user import UserListSerializer

class UserGroupSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserGroup
		fields = ['gid', 'group_name', 'description', 'users']

class UserGroupReadOnlySerializer(UserGroupSerializer):
	"""
	Extend from UserGroupSerializer with detail of every user
	"""
	users = UserListSerializer(many=True, read_only=True)
