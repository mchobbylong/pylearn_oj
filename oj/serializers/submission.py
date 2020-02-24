from rest_framework import serializers
from oj.models import Submission, Test, Task
from datetime import datetime

class SubmissionListSerializer(serializers.ModelSerializer):
	"""
	Read-only serializer for list of submissions
	"""
	status = serializers.SerializerMethodField()

	class Meta:
		model = Submission
		fields = ['sid', 'problem', 'user', 'status', 'score', 'full_score', 'is_solution', 'submit_time']

	def get_status(self, submission):
		return submission.status(self.context['request'])

class SubmissionDetailSerializer(SubmissionListSerializer):
	"""
	Read-only serializer for detail of a submission
	"""
	result = serializers.SerializerMethodField()

	class Meta:
		model = Submission
		fields = ['sid', 'problem', 'user', 'status', 'score', 'full_score', 'result', 'code', 'submit_time']

	def get_result(self, submission):
		# If status in ['pending', 'running', 'system_error']
		# then no output
		result = submission.result
		if (not result) or (result == 'running') or (result == 'system_error'):
			return []

		result = json.loads(result)
		show_first_wrong = True
		for test in result:
			if not (self.context['request'].user.is_superuser or (show_first_wrong and test['score'] == 0)):
				test.pop('output')
			show_first_wrong = show_first_wrong and (not hasattr(test, 'output'))
		return result

class SubmissionSubmitSerializer(serializers.ModelSerializer):
	class Meta:
		model = Submission
		fields = ['sid', 'problem', 'code']

	def create(self, validated_data):
		user = self.context['request'].user
		sub = Submission(user=user, **validated_data)
		sub.save()
		sub.tasks.set(Task.objects.filter(
			deadline__gt=datetime.now(),
			problems=sub.problem,
			usergroups__users=user,
		))
		return sub
