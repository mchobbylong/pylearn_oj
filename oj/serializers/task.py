from rest_framework import serializers
from oj.models import Task, Problem, Submission

class ProblemOutlineSerializer(serializers.ModelSerializer):
	status_in_task = serializers.SerializerMethodField()

	class Meta:
		model = Problem
		fields = ['pid', 'title', 'level', 'status_in_task']

	def get_status_in_task(self, problem):
		sub = self.context['task'].submissions.filter(problem=problem, user=self.context['request'].user).order_by('-score').first()
		if sub:
			sub = sub.status(self.context['request'])
		return sub

class TaskSerializer(serializers.ModelSerializer):
	class Meta:
		model = Task
		fields = ['task_id', 'task_name', 'description', 'problems', 'deadline']

class TaskReadOnlySerializer(TaskSerializer):
	problems = serializers.SerializerMethodField()

	def get_problems(self, task):
		context = self.context
		context['task'] = task
		return ProblemOutlineSerializer(task.problems, many=True, context=context).data
