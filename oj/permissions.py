from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated as IsLogin

class ReadOnly(permissions.BasePermission):
	def has_permission(self, request, view):
		return request.method in permissions.SAFE_METHODS

class IsAdmin(permissions.BasePermission):
	def has_permission(self, request, view):
		return request.user.is_superuser
	def has_object_permission(self, request, view, obj):
		return request.user.is_superuser

class IsCurrentUser(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if obj.__class__.__name__ == 'User':
			return obj == request.user
		if hasattr(obj, 'user'):
			return obj.user == request.user
		if hasattr(obj, 'users'):
			return obj.users.filter(pk=request.user.id).exists()
		return False
