from rest_framework import serializers
from oj.models import TestSet, Test
from .test import TestSerializer

class TestSetSerializer(serializers.ModelSerializer):
	full_score = serializers.FloatField(read_only=True)
	tests = TestSerializer(many=True)

	class Meta:
		model = TestSet
		fields = '__all__'

	def create(self, validated_data):
		tests_data = validated_data.pop('tests')
		# Calculate full score & create testset
		full_score = 0
		for test in tests_data:
			full_score += test['score']
		testset = TestSet.objects.create(full_score=full_score, **validated_data)
		# Create tests
		tests = []
		for test_data in tests_data:
			test = Test(**test_data)
			test.save()
			tests.append(test)
		testset.tests.set(tests)
		testset.problem.testset = testset
		testset.problem.save()
		return testset

	def update(self, testset, validated_data):
		tests_data = validated_data.pop('tests')
		# Update tests
		tests = []
		full_score = 0
		for test_data in tests_data:
			try:
				test = Test.objects.get(**test_data)
			except Test.DoesNotExist:
				test_data.pop('test_id')
				test = Test.objects.create(**test_data)
			full_score += test.score
			tests.append(test)
		# Compare with current tests & update
		if set(testset.tests.all()) != set(tests):
			testset.pk = None
			testset.full_score = full_score
			testset.save()
			testset.tests.set(tests)
			testset.problem.testset = testset
			testset.problem.save()
		return testset
