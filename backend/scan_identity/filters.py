from abc import ABC

from rest_framework.filters import BaseFilterBackend
import coreapi


class RangeFilterBackend(BaseFilterBackend, ABC):   # RangeFilterBackend is used to get range
    def get_schema_fields(self, view):              # This method is used to get schema fields for swagger
        return [coreapi.Field(                      # Field from
            name='from',
            location='query',
            required=True,
            type='integer',
            description='ID from which to start the query',
            example=1,
        ), coreapi.Field(                           # Field to
            name='to',
            location='query',
            required=True,
            type='integer',
            description='ID at which to end the query',
            example=100,
        )]
