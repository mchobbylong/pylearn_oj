from rest_framework import viewsets
from django_filters import rest_framework as filters
from oj.models import UserGroup
from oj.serializers import UserGroupSerializer, UserGroupReadOnlySerializer
from oj.permissions import IsAdmin, IsCurrentUser, IsLogin

class UserGroupFilter(filters.FilterSet):
	group_name = filters.CharFilter(lookup_expr='icontains')
	class Meta:
		model = UserGroup
		fields = ['group_name']

class UserGroupViewSet(viewsets.ModelViewSet):
	queryset = UserGroup.objects.all()
	filterset_class = UserGroupFilter

	def get_permissions(self):
		if self.action in ['list', 'retrieve']:
			return [IsLogin(), (IsAdmin|IsCurrentUser)()]
		return [IsAdmin()]

	def get_serializer_class(self):
		if self.action in ['list', 'retrieve']:
			return UserGroupReadOnlySerializer
		return UserGroupSerializer
