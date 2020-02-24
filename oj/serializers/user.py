from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer
from oj.models import User

class UserListSerializer(serializers.ModelSerializer):
	"""
	Serializer to create, list and delete users
	"""
	password = serializers.CharField(write_only=True, required=True)

	class Meta:
		model = User
		fields = ['id', 'username', 'password']

	def create(self, validated_data):
		user = super().create(validated_data)
		user.set_password(validated_data['password'])
		user.save()
		return user

	def update(self, instance, validated_data):
		user = super().update(instance, validated_data)
		try:
			user.set_password(validated_data['password'])
			user.save()
		except KeyError:
			pass
		return user

class UserProfileSerializer(serializers.ModelSerializer):
	"""
	Serializer to retrieve and update user profile
	"""
	item_per_page = serializers.IntegerField(min_value=1, max_value=100)
	avatar = VersatileImageFieldSerializer(required=False, sizes='user_avatar')

	class Meta:
		model = User
		fields = ['id', 'username', 'item_per_page', 'avatar']

class PasswordSerializer(serializers.Serializer):
	"""
	Serializer to change an user's password
	"""
	old_password = serializers.CharField(required=False)
	new_password = serializers.CharField(required=True)
