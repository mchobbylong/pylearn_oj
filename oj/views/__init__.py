from .user import UserList, UserDetail, UserChangePassword
from .usergroup import UserGroupViewSet
from .task import TaskViewSet
from .tag import TagViewSet
from .announcement import AnnouncementViewSet
from .problem import ProblemViewSet
from .submission import SubmissionViewSet
from .testset import TestSetViewSet

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'users': reverse('user-list', request=request, format=format),
		'usergroups': reverse('usergroup-list', request=request, format=format),
		'tasks': reverse('task-list', request=request, format=format),
	})
