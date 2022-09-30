from abc import ABC

from rest_framework.filters import BaseFilterBackend
import coreapi


class RangeFilterBackend(BaseFilterBackend, ABC):
    def get_schema_fields(self, view):
        return [coreapi.Field(
            name='from',
            location='query',
            required=True,
            type='integer',
            description='ID from which to start the query',
            example=1,
        ), coreapi.Field(
            name='to',
            location='query',
            required=True,
            type='integer',
            description='ID at which to end the query',
            example=100,
        )]
