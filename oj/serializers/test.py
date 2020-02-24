from rest_framework import serializers
from oj.models import Test

class TestSerializer(serializers.ModelSerializer):
	# To show test_id in validated_data explicitly
	test_id = serializers.ModelField(Test()._meta.get_field('test_id'))

	class Meta:
		model = Test
		fields = '__all__'
