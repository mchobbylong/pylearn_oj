from rest_framework import serializers
from oj.models import Problem
from .tag import TagSerializer
from .submission import SubmissionDetailSerializer

class ProblemSerializer(serializers.ModelSerializer):
	level = serializers.ChoiceField([1, 2, 3])
	testset = serializers.PrimaryKeyRelatedField(read_only=True)
	ac_rate = serializers.ReadOnlyField()
	high_score_sub = serializers.SerializerMethodField()
	latest_code = serializers.SerializerMethodField()

	class Meta:
		model = Problem
		fields = '__all__'

	def get_high_score_sub(self, problem):
		submissions = problem.submissions.filter(user=self.context['request'].user).order_by('-score', '-sid').all()
		for sub in submissions:
			data = SubmissionDetailSerializer(sub, context=self.context).data
			if data['status'] == 'hidden':
				continue
			return {
				'sid': data['sid'],
				'status': data['status'],
				'score': data['score'],
			}
		return None

	def get_latest_code(self, problem):
		submission = problem.submissions.filter(user=self.context['request'].user).first()
		if submission:
			submission = submission.code
		return submission

class ProblemReadOnlySerializer(ProblemSerializer):
	"""
	Extend from ProblemSerializer with tags' names
	"""
	# tags = TagSerializer(many=True, read_only=True)
	tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='tag_name')
