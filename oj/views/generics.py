from rest_framework import serializers, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from oj.permissions import IsAdmin, IsLogin

class CommonViewSet(ModelViewSet):
	def get_permissions(self):
		if self.action in ['list', 'retrieve']:
			return [IsLogin()]
		return [IsAdmin()]

class RejudgeSerializer(serializers.Serializer):
	count = serializers.BooleanField(required=True)

class RejudgeMixin:
	"""
	Rejudge related submissions
	"""
	@action(
		detail=True,
		methods=['post'],
		serializer_class=RejudgeSerializer,
		permission_classes=[IsAdmin],
	)
	def rejudge(self, request, *args, **kwargs):
		sub = self.get_object()
		if hasattr(sub, 'submissions'):
			sub_list = sub.submissions
			count = sub_list.count()
		else:
			sub_list = [sub]
			count = 1
		# Check if client wants to get the count
		serializer = RejudgeSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		if serializer.validated_data['count']:
			response = { 'count': count }
			return Response(response)
		for sub in sub_list:
			# Send to judger
			pass
		return Response(status=status.HTTP_204_NO_CONTENT)
