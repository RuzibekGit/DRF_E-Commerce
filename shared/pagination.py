from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response



class CustomPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 50

    def get_paginated_response(self, data):
        response = {
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "page_size": self.get_page_size(),
            "count": self.page.paginator.count,
            "results": data
        }
        return Response(response)