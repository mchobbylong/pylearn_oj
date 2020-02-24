from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('problems', views.ProblemViewSet, basename='problem')
router.register('submissions', views.SubmissionViewSet, basename='submission')
router.register('testsets', views.TestSetViewSet)
router.register('tags', views.TagViewSet)
router.register('usergroups', views.UserGroupViewSet)
router.register('announcements', views.AnnouncementViewSet)
router.register('tasks', views.TaskViewSet, basename='task')

urlpatterns = [
	path('', include(router.urls)),
	path('users/', views.UserList.as_view(), name='user-list'),
	path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
	path('users/<int:pk>/change_password/', views.UserChangePassword.as_view(), name='user-change-password'),
]
