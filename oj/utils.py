from rest_framework.pagination import PageNumberPagination

class ExtendedPageNumberPagination(PageNumberPagination):
	page_size_query_param = 'size'
	max_page_size = 100
