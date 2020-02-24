from rest_framework import mixins, viewsets, status, response
from rest_framework.permissions import BasePermission
from rest_framework.decorators import action
from rest_framework.serializers import Serializer
from oj.views.generics import RejudgeMixin, RejudgeSerializer
from oj.models import Submission
from oj.serializers import SubmissionListSerializer, SubmissionDetailSerializer, SubmissionSubmitSerializer
from oj.permissions import IsAdmin, IsCurrentUser, IsLogin

class IsSubmissionShown(BasePermission):
	def has_object_permission(self, request, view, submission):
		# return (IsNotHidden and (IsCurrentUser or IsSolution))
		return submission.status(request) != 'hidden' and (submission.user == request.user or submission.is_solution)

class SubmissionViewSet(viewsets.GenericViewSet,
	mixins.ListModelMixin,
	mixins.CreateModelMixin,
	mixins.RetrieveModelMixin,
	mixins.DestroyModelMixin,
	RejudgeMixin,
):

	def get_queryset(self):
		queryset = Submission.objects.all()
		if not self.request.user.is_superuser:
			queryset = queryset.filter(problem__visible=True)
		return queryset

	def get_serializer_class(self):
		if self.action == 'list':
			return SubmissionListSerializer
		if self.action == 'retrieve':
			return SubmissionDetailSerializer
		if self.action == 'mark_as_solution':
			return Serializer
		if self.action in ['rejudge', 'rejudge_pending']:
			return RejudgeSerializer
		return SubmissionSubmitSerializer

	def get_permissions(self):
		if self.action == 'retrieve':
			return [IsLogin(), (IsAdmin|IsSubmissionShown)()]
		elif self.action in ['list', 'create']:
			return [IsLogin()]
		return [IsAdmin()]

	def perform_create(self, serializer):
		submission = serializer.save()
		# Send to judger

	@action(detail=True, methods=['post'])
	def mark_as_solution(self, request, *args, **kwargs):
		submission = self.get_object()
		submission.is_solution = not submission.is_solution
		submission.save()
		return response.Response(status=status.HTTP_204_NO_CONTENT)

	@action(detail=False, methods=['post'])
	def rejudge_pending(self, request, *args, **kwargs):
		submissions = Submission.objects.filter(result='').all()
		serializer = RejudgeSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		if serializer.validated_data['count']:
			return response.Response({ 'count': submissions.count() }, status=status.HTTP_204_NO_CONTENT)
		# Send to judger
		return response.Response(status=status.HTTP_204_NO_CONTENT)
