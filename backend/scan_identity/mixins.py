from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response


class RangeMixin:                                       # Mixin to handle range
    @staticmethod
    def queryset_limit_offset(queryset, request):       # method to filter queryset by range
        start = request.query_params.get('from', None)
        end = request.query_params.get('to', None)
        if start and end:
            queryset = queryset.filter(id__range=[start, end])
            return queryset
        else:
            raise ValueError('Missing "from" and "to" query parameters')

    def list(self, request, *args, **kwargs):           # method to handle GET request
        """
            from -- ID from which to start the query
            to -- ID at which to end the query
        """
        try:
            queryset = self.queryset_limit_offset(self.get_queryset(), request)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

