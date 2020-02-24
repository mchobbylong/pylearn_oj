from oj.views.generics import CommonViewSet, RejudgeMixin
from oj.models import Problem
from oj.serializers import ProblemSerializer, ProblemReadOnlySerializer
from django_filters import rest_framework as filters

class ProblemFilter(filters.FilterSet):
	title = filters.CharFilter(lookup_expr='icontains')
	class Meta:
		model = Problem
		fields = ['title', 'level', 'tags__tag_id']

class ProblemViewSet(RejudgeMixin, CommonViewSet):
	filterset_class = ProblemFilter

	def get_queryset(self):
		queryset = Problem.objects.all()
		if not self.request.user.is_superuser:
			queryset = queryset.filter(visible=True)
		return queryset

	def get_serializer_class(self):
		if self.action in ['list', 'retrieve']:
			return ProblemReadOnlySerializer
		return ProblemSerializer
