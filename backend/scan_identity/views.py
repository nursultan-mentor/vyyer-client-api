from asgiref.sync import sync_to_async
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
import aiohttp
import json
import asyncio
from aiohttp import web
from itertools import chain

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
        "Authorization": "Bearer "
                         "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IncyYVl6R0I2OG9LeVQxV1dyTnB5MSJ9.eyJpc3MiOiJodHRwczovL3Z5eWVyLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MTYwODY5OGY1YTQwMzAwNjhjZjYzNmUiLCJhdWQiOiJodHRwczovL3Rlc3QtdW5pZmllZC5jbGllbnQtYXBpLnZ5eWVyLmlkIiwiaWF0IjoxNjY0NTE3MzA5LCJleHAiOjE2NjUxMjIxMDksImF6cCI6ImpjU3o3N0Y4ZHljUGdlZFdTZ3JwM0R4Q1E3cXZZSXZDIiwiZ3R5IjoicGFzc3dvcmQiLCJwZXJtaXNzaW9ucyI6WyJmYWNlbWF0Y2g6d29ya2Zsb3dzdGF0ZSIsImxpdmVsaW5lc3M6d29ya2Zsb3dzdGF0ZSIsInB1bGw6aWRlbnRpdGllcyIsInB1bGw6c2NhbnMiLCJyZWFkOmNvdW50cmllcyIsInJlYWQ6Y291bnRyaWVzLXJhbmdlIiwicmVhZDpjb3VudHJ5LWJ5LWlkIiwicmVhZDpjb3VudHJ5LWluZm8iLCJyZWFkOmNvdW50cnktbWV0YSIsInJlYWQ6aWRlbnRpdGllcyIsInJlYWQ6aWRlbnRpdGllcy1yYW5nZSIsInJlYWQ6aWRlbnRpdHktYXZhdGFyIiwicmVhZDppZGVudGl0eS1ieS1pZCIsInJlYWQ6aWRlbnRpdHktaW5mbyIsInJlYWQ6aWRlbnRpdHktbWV0YSIsInJlYWQ6bGljZW5zZS1hbmRyb2lkIiwicmVhZDpsaWNlbnNlLWluZm8iLCJyZWFkOmxpY2Vuc2UtaW9zIiwicmVhZDpsaWNlbnNlLW1ldGEiLCJyZWFkOmxpY2Vuc2Utd2ViIiwicmVhZDpyZWYtbWV0YSIsInJlYWQ6cmVmLXNjYW5zIiwicmVhZDpyZWYtdXNlcnMiLCJyZWFkOnNjYW4tYnktaWQiLCJyZWFkOnNjYW4taW5mbyIsInJlYWQ6c2Nhbi1tZXRhIiwicmVhZDpzY2FucyIsInJlYWQ6c2NhbnMtcmFuZ2UiLCJyZWFkOnN0YXRlLWJ5LWlkIiwicmVhZDpzdGF0ZWhvbGlkYXktYnktaWQiLCJyZWFkOnN0YXRlaG9saWRheS1pbmZvIiwicmVhZDpzdGF0ZWhvbGlkYXktbWV0YSIsInJlYWQ6c3RhdGVob2xpZGF5cyIsInJlYWQ6c3RhdGVob2xpZGF5cy1yYW5nZSIsInJlYWQ6c3RhdGUtaW5mbyIsInJlYWQ6c3RhdGUtbWV0YSIsInJlYWQ6c3RhdGVzIiwicmVhZDpzdGF0ZXMtcmFuZ2UiLCJyZWFkOndvcmtmbG93cyIsInJlYWQ6d29ya2Zsb3dzdGF0ZSIsInJlZ2lzdGVyOndvcmtmbG93c3RhdGUiLCJzY2FuOndvcmtmbG93c3RhdGUiLCJzZWFyY2g6aWRlbnRpdGllcyIsInNlYXJjaDpzY2FucyIsIndyaXRlOmlkZW50aXRpZXMiLCJ3cml0ZTppZGVudGl0eS1ieS1pZCIsIndyaXRlOnNjYW4iLCJ3cml0ZTpzY2FuLWltYWdlIiwid3JpdGU6d29ya2Zsb3ciLCJ3cml0ZTp3b3JrZmxvd3N0YXRlLWltYWdlIl19.sUzFl4IOxSk29ufp1nC7_A2_QVc8hReDiQM9A3dJwmPdOT2_c8r7i7lJCFPPTF0MKvX3D5KtlZqLdiCksaTlvPCgwUE8oI7j5jYCTjmApOIvk1g81jev0OGIUwudIwYm0TyfNJMIJG0DfbVhx7Mzd-j8Brp707xBLsA4tKcOPLwej4xZhL8_-flwkDqjATsJxAFgBJGhI3aLgP7I97fLQ-rnljGCwlm2t28aH2mNe790wG2bnlglF06gVl_SwCDewtlsBK_bIUFsI4LQCTViZoM7dh2hK5nO2rF64Fj9JQ1VPaUPU4cw9E2JhVAgW1kwBGMBnKtbKxa2NOCRYsatXw",
        "X-User-Id": "Auth0User",
        "X-Org-Id": "Auth0Org"
    }
    async with aiohttp.ClientSession() as session:
        scan_url = '/api/v2/scans/get/'
        identity_url = '/api/v2/identities/get/'
        tasks = (get_data(session, headers, dict(Page=c, PerPage=25), scan_url) for c in range(1, 100))
        result = await asyncio.gather(*tasks)

        all_data = tuple(chain(res['Data'] for res in result))

        identity_ids = list({i.get('IdentityID') for i in all_data if i.get('IdentityID')})

        identity_tasks = []
        for i in range(0, len(identity_ids), 100):
            j = i + 100
            identity_tasks.append(get_data(session, headers, dict(IdentityIDs=identity_ids[i:j]), identity_url))
        identity_tasks.append(get_data(session, headers, dict(IdentityIDs=identity_ids[j:]), identity_url))
        identity_result = await asyncio.gather(*identity_tasks)

        all_identity_data = tuple(chain(res['Data'] for res in identity_result))

        identity_bulk_create = (Identity(id=i['ID'],
                                         uid=i['UID'],
                                         fullname=i['FullName'],
                                         issued_at=i.get('IssuedAt', None),
                                         expires_at=i.get('ExpiresAt', None)) for i in all_identity_data)

        scan_bulk_create = (Scan(id=i['ID'],
                                 identity_id=i['IdentityID'],
                                 user_id=i['UserID'],
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
