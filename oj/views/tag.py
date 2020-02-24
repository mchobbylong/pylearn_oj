from oj.views.generics import CommonViewSet
from oj.models import Tag
from oj.serializers import TagSerializer

class TagViewSet(CommonViewSet):
	queryset = Tag.objects.all()
	serializer_class = TagSerializer
