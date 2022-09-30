from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import RangeFilterBackend
from .mixins import RangeMixin
from .models import Identity, Scan
from .paginations import RangePagination
from .serializers import IdentitySerializer, ScanSerializer
from .tasks import populate_data


@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Identity GetList']))
class IdentityListAPIView(ListAPIView):                             # GET /identity/get/
    """Get list of identities"""
    queryset = Identity.objects.all()
    serializer_class = IdentitySerializer
    filter_backends = [OrderingFilter, ]
    ordering_fields = ['issued_at', 'expires_at']                   # ?ordering=issued_at


@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Identity GetByID']))
class IdentityDetailAPIView(RetrieveAPIView):                       # GET /identity/get/<int:pk>/
    """Get identity by id"""
    queryset = Identity.objects.all()
    serializer_class = IdentitySerializer


@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Scan GetList']))
class ScanListAPIView(ListAPIView):                                 # GET /scan/get/
    """Get list of scans"""
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer
    filter_backends = [OrderingFilter, ]
    ordering_fields = ['id', 'identity_id']                         # ?ordering=id


@method_decorator(name='get', decorator=swagger_auto_schema(tags=['Scan GetByID']))
class ScanDetailAPIView(RetrieveAPIView):                           # GET /scan/get/<int:pk>/
    """Get scan by id"""
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer


class ScanListRangeAPIView(RangeMixin, ScanListAPIView):            # GET /scan/range/
    """Get list of scans by range"""                                # RangeMixin is used to get range
    pagination_class = RangePagination
    filter_backends = [RangeFilterBackend, ]


class IdentityListRangeAPIView(RangeMixin, IdentityListAPIView):    # GET /identity/range/
    """Get list of identities by range"""                           # RangeMixin is used to get range
    pagination_class = RangePagination
    filter_backends = [RangeFilterBackend, ]


class GenerateData(APIView):                                        # GET /generate_data/
    """Get data from Client API"""

    def get(self, request):
        populate_data.delay()                                       # Run task to populate data
        return Response({'status': 'Data Generation Started'}, status=status.HTTP_200_OK)
