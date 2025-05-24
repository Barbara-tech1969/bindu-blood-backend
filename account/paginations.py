from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
class UserProfilePagination(PageNumberPagination):
    page_size = 12
    page_query_param = "p"
    page_size_query_param = "records"
    max_page_size = 40
    def get_paginated_response(self, data):
        return Response({
            'total_objects': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page_number': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })