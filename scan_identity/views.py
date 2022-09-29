from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
import aiohttp
import asyncio

from .models import Identity, Scan
from .serializers import IdentitySerializer, ScanSerializer


class IdentityListAPIView(ListAPIView):
    queryset = Identity.objects.all()
    serializer_class = IdentitySerializer


class IdentityDetailAPIView(RetrieveAPIView):
    queryset = Identity.objects.all()
    serializer_class = IdentitySerializer


class ScanListAPIView(ListAPIView):
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer


class ScanDetailAPIView(RetrieveAPIView):
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer


def queryset_limit_offset(queryset, request):
    start = request.query_params.get('from', None)
    end = request.query_params.get('to', None)
    if start and end:
        queryset = queryset.filter(id__range=[start, end])
        return queryset
    else:
        raise ValueError('Missing "from" and "to" query parameters')


class ScanListRangeAPIView(ScanListAPIView):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset_limit_offset(queryset, self.request)


class IdentityListRangeAPIView(IdentityListAPIView):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset_limit_offset(queryset, self.request)




