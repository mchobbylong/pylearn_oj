from rest_framework import serializers
from oj.models import Announcement
from .user import UserListSerializer

class AnnouncementSerializer(serializers.ModelSerializer):
	user = UserListSerializer(read_only=True)
	publish_time = serializers.DateTimeField(read_only=True)

	class Meta:
		model = Announcement
		fields = '__all__'
