from rest_framework.viewsets import ModelViewSet
from oj.models import TestSet
from oj.serializers import TestSetSerializer
from oj.permissions import IsAdmin, IsLogin

class TestSetViewSet(ModelViewSet):
	queryset = TestSet.objects.all()
	serializer_class = TestSetSerializer
	permission_classes = [IsAdmin]
