from rest_framework import serializers
from oj.models import Tag

class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = '__all__'
