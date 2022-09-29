from asgiref.sync import sync_to_async
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
import aiohttp
import json
import asyncio
from aiohttp import web

from .models import Identity, Scan
from .serializers import IdentitySerializer, ScanSerializer


async def get_data(session, headers, data, url):
    Audience = 'https://test-unified.client-api.vyyer.id'
    async with session.post(f'{Audience}{url}', headers=headers, json=data) as response:
        data_json = await response.json()
        return data_json


def delete_data():
    Scan.objects.all().delete()
    Identity.objects.all().delete()


async def generate_data(request):
    headers = {
        "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IncyYVl6R0I2OG9LeVQxV1dyTnB5MSJ9.eyJpc3MiOiJodHRwczovL3Z5eWVyLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTYwODY5OGY1YTQwMzAwNjhjZjYzNmUiLCJhdWQiOiJodHRwczovL3Rlc3QtdW5pZmllZC5jbGllbnQtYXBpLnZ5eWVyLmlkIiwiaWF0IjoxNjY0NDMyNzk1LCJleHAiOjE2NjUwMzc1OTUsImF6cCI6ImpjU3o3N0Y4ZHljUGdlZFdTZ3JwM0R4Q1E3cXZZSXZDIiwiZ3R5IjoicGFzc3dvcmQiLCJwZXJtaXNzaW9ucyI6WyJmYWNlbWF0Y2g6d29ya2Zsb3dzdGF0ZSIsImxpdmVsaW5lc3M6d29ya2Zsb3dzdGF0ZSIsInB1bGw6aWRlbnRpdGllcyIsInB1bGw6c2NhbnMiLCJyZWFkOmNvdW50cmllcyIsInJlYWQ6Y291bnRyaWVzLXJhbmdlIiwicmVhZDpjb3VudHJ5LWJ5LWlkIiwicmVhZDpjb3VudHJ5LWluZm8iLCJyZWFkOmNvdW50cnktbWV0YSIsInJlYWQ6aWRlbnRpdGllcyIsInJlYWQ6aWRlbnRpdGllcy1yYW5nZSIsInJlYWQ6aWRlbnRpdHktYXZhdGFyIiwicmVhZDppZGVudGl0eS1ieS1pZCIsInJlYWQ6aWRlbnRpdHktaW5mbyIsInJlYWQ6aWRlbnRpdHktbWV0YSIsInJlYWQ6bGljZW5zZS1hbmRyb2lkIiwicmVhZDpsaWNlbnNlLWluZm8iLCJyZWFkOmxpY2Vuc2UtaW9zIiwicmVhZDpsaWNlbnNlLW1ldGEiLCJyZWFkOmxpY2Vuc2Utd2ViIiwicmVhZDpyZWYtbWV0YSIsInJlYWQ6cmVmLXNjYW5zIiwicmVhZDpyZWYtdXNlcnMiLCJyZWFkOnNjYW4tYnktaWQiLCJyZWFkOnNjYW4taW5mbyIsInJlYWQ6c2Nhbi1tZXRhIiwicmVhZDpzY2FucyIsInJlYWQ6c2NhbnMtcmFuZ2UiLCJyZWFkOnN0YXRlLWJ5LWlkIiwicmVhZDpzdGF0ZWhvbGlkYXktYnktaWQiLCJyZWFkOnN0YXRlaG9saWRheS1pbmZvIiwicmVhZDpzdGF0ZWhvbGlkYXktbWV0YSIsInJlYWQ6c3RhdGVob2xpZGF5cyIsInJlYWQ6c3RhdGVob2xpZGF5cy1yYW5nZSIsInJlYWQ6c3RhdGUtaW5mbyIsInJlYWQ6c3RhdGUtbWV0YSIsInJlYWQ6c3RhdGVzIiwicmVhZDpzdGF0ZXMtcmFuZ2UiLCJyZWFkOndvcmtmbG93cyIsInJlYWQ6d29ya2Zsb3dzdGF0ZSIsInJlZ2lzdGVyOndvcmtmbG93c3RhdGUiLCJzY2FuOndvcmtmbG93c3RhdGUiLCJzZWFyY2g6aWRlbnRpdGllcyIsInNlYXJjaDpzY2FucyIsIndyaXRlOmlkZW50aXRpZXMiLCJ3cml0ZTppZGVudGl0eS1ieS1pZCIsIndyaXRlOnNjYW4iLCJ3cml0ZTpzY2FuLWltYWdlIiwid3JpdGU6d29ya2Zsb3ciLCJ3cml0ZTp3b3JrZmxvd3N0YXRlLWltYWdlIl19.tp0O69zxruSbkmSutUV0874wYHRWSGsHmiKwFUe9v7 - LKgBxuSr5zzcy8tNIfyT9EbR6Ip5b6SA0pCWNbujf60Ef - v9J1HRuGcx1BxLrIi6eGKu - uvUKa6rLJ9FRA57dx4pcYtBUDBSlroF0f_FmSntEk9IA2iSESqUJk9bXWx1VxE8pGqsDI1TGenvB75EkB4oiFv8ob3erubZAjIQk0zuS20i4CA3kNQm0oD4ySgGfbGoCqg6CMKmQbOtlf - ItYxTzzYghTVGwOakewrYvfxAzhY3X_9Aa0NJd5B8NvFiQyZWxUQgRZ1v1CohufHrhODT8rpsYXre47Su6He_6dg",
        "X-User-Id": "Auth0User",
        "X-Org-Id": "Auth0Org"
    }
    async with aiohttp.ClientSession() as session:
        scan_url = '/api/v2/scans/get/'
        identity_url = '/api/v2/identities/get/'
        tasks = (get_data(session, headers, dict(Page=c, PerPage=25), scan_url) for c in range(1, 100))
        result = await asyncio.gather(*tasks)

        all_data = []
        for res in result:
            all_data.extend(res['Data'])

        identity_ids = {i['IdentityID'] for i in all_data}
        identity_result = await get_data(session, headers, dict(IDs=list(identity_ids)), identity_url)

        identity_bulk_create = (Identity(id=i['ID'],
                                         uid=i['UID'],
                                         fullname=i['FullName'],
                                         issued_at=i.get('IssuedAt', None),
                                         expires_at=i.get('ExpiresAt', None)) for i in identity_result['Data'])

        scan_bulk_create = (Scan(id=i['ID'],
                                 identity_id=i['IdentityID'],
                                 user_id=i['UserID'],
                                 created_at=i['CreatedAt'],
                                 flags=i['Flags'],
                                 verdict_type=i['VerdictType'],
                                 verdict_result=i['VerdictResult'],
                                 verdict_name=i['VerdictName'],
                                 verdict_value=i['VerdictValue']) for i in all_data)

        await sync_to_async(delete_data)()
        await Identity.objects.abulk_create(identity_bulk_create)
        await Scan.objects.abulk_create(scan_bulk_create)
        return HttpResponse('Data generated')


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
