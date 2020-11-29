from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    page_size = 25
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('total_pages', self.page.paginator.num_pages),
            ('page_size', self.get_page_size(self.request)),
            ('records', len(data)),
            ('current', self.page.number),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
            ('lastPage', self.page.paginator.count),
            ('countItemsOnPage', self.page_size),
        ]))
