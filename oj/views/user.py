from django.db.models import Value
from django.db.models.functions import Length, Replace
from django.contrib.auth import update_session_auth_hash
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from django_filters import rest_framework as filters
from oj.serializers import UserListSerializer, UserProfileSerializer, PasswordSerializer
from oj.models import User
from oj.permissions import IsLogin, IsCurrentUser, IsAdmin

class SearchUserFilter(filters.FilterSet):
	username = filters.CharFilter(method='filter_username')
	class Meta:
		model = User
		fields = ['username']
	def filter_username(self, queryset, name, value):
		# Order the queryset by the relevance of username
		return queryset.filter(username__icontains=value).order_by(Length(Replace('username', Value(value))))

class UserList(generics.ListCreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserListSerializer
	filterset_class = SearchUserFilter

	def get_permissions(self):
		if self.request.method != 'GET':
			return [IsAdmin()]
		return [IsLogin()]

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = User.objects.all()
	serializer_class = UserProfileSerializer
	permission_classes = [IsLogin, IsAdmin|IsCurrentUser]

	def perform_update(self, serializer):
		old_username = self.get_object().username
		if not self.request.user.is_superuser and serializer.validated_data['username'] != old_username:
			raise ValidationError('You cannot change username')
		serializer.save()

class UserChangePassword(generics.UpdateAPIView):
	queryset = User.objects.all()
	serializer_class = PasswordSerializer
	permission_classes = [IsLogin, IsAdmin|IsCurrentUser]

	def update(self, request, *args, **kwargs):
		user = self.get_object()
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		# Check old password
		if (not request.user.is_superuser) and (not user.check_password(serializer.validated_data.get('old_password'))):
			raise ValidationError('Wrong old password')
		# Set new password
		user.set_password(serializer.validated_data['new_password'])
		user.save()
		# Refresh token for current user
		if user == request.user:
			update_session_auth_hash(request, user)
		return Response(status=status.HTTP_204_NO_CONTENT)
