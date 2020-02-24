from oj.views.generics import CommonViewSet, RejudgeMixin, RejudgeSerializer
from oj.serializers import TaskSerializer, TaskReadOnlySerializer
from oj.models import Task

class TaskViewSet(RejudgeMixin, CommonViewSet):

	def get_queryset(self):
		queryset = Task.objects.all()
		if not self.request.user.is_superuser:
			queryset = queryset.filter(usergroups__users=self.request.user)
		return queryset

	def get_serializer_class(self):
		if self.action in ['list', 'retrieve']:
			return TaskReadOnlySerializer
		if self.action == 'rejudge':
			return RejudgeSerializer
		return TaskSerializer
