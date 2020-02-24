from oj.views.generics import CommonViewSet
from oj.models import Announcement
from oj.serializers import AnnouncementSerializer

class AnnouncementViewSet(CommonViewSet):
	queryset = Announcement.objects.all()
	serializer_class = AnnouncementSerializer

	def perform_create(self, serializer):
		serializer.save(user=self.request.user)
