from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
        This is responsible for pagination. The page size,
        and maximum page are specified here.
    """

    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000

    # Todo: Make this more dynamic in the future
