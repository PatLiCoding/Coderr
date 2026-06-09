from rest_framework.pagination import PageNumberPagination


class OfferPagination(PageNumberPagination):
    """
    Custom page-number based pagination for Offer lists.

    Controls the number of offers returned per API request and allows clients
    to dynamically adjust the page size via a query parameter.

    Attributes:
        page_size (int): The default number of items to return per page
                        (Default: 6).
        page_size_query_param (str): The name of the query parameter that
                        allows the client to set a custom page size
                        (e.g., `?page_size=10`).
    """
    page_size = 6
    page_size_query_param = 'page_size'
