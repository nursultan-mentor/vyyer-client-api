import asyncio
from itertools import chain

import aiohttp
from asgiref.sync import sync_to_async
from celery import shared_task

from .audience import Audience, auth_data, base_headers
from .models import Identity, Scan


# Async function to get data from API using post method
# and return the data in json format
async def get_data(session, headers, data, url):
    async with session.post(f'{Audience}{url}', headers=headers, json=data) as response:
        data_json = await response.json()
        return data_json


# Delete all data from database
def delete_data():
    Scan.objects.all().delete()
    Identity.objects.all().delete()


# Get auth token from API and return the header with token
async def get_auth_token():
    url = 'https://vyyer.us.auth0.com/oauth/token/'

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=base_headers, data=auth_data) as response:
            data = await response.json()
            print(data)
            auth = {
                'Authorization': f'{data["token_type"]} {data["access_token"]}'
            }
            return auth


# Get data from API and populate the database
async def generate_data():
    # Get header with auth token
    auth = await get_auth_token()
    # Update header with auth token
    headers = {**base_headers, **auth}
    # Gather tasks to run with session
    async with aiohttp.ClientSession() as session:
        scan_url = '/api/v2/scans/get/'
        identity_url = '/api/v2/identities/get/'

        # store tasks to get all scans in a list per 20 scans per request
        tasks = (get_data(session, headers, dict(Page=c, PerPage=20), scan_url) for c in range(1, 3))
        result = await asyncio.gather(*tasks)

        # store all scan results in a tuple
        all_data = tuple(chain.from_iterable(res['Data'] for res in result))

        # getting all identity ids from all scans and store them in a set to remove duplicates
        # and store them in a list to be able to slice them
        identity_ids = list({i.get('IdentityID') for i in all_data if i.get('IdentityID')})

        # store tasks to get all identities in a list per 25 identities per request
        identity_tasks = []
        for i in range(0, len(identity_ids), 25):
            j = i + 25
            identity_tasks.append(get_data(session, headers, dict(IdentityIDs=identity_ids[i:j]), identity_url))
        identity_tasks.append(get_data(session, headers, dict(IdentityIDs=identity_ids[j:]), identity_url))

        identity_result = await asyncio.gather(*identity_tasks)

        # store all identity results in a tuple
        all_identity_data = tuple(chain(res['Data'] for res in identity_result))

        # Prepare bulk create tuple to save all Identity objects
        identity_bulk_create = (Identity(id=i['ID'],
                                         uid=i['UID'],
                                         fullname=i['FullName'],
                                         issued_at=i.get('IssuedAt', None),
                                         expires_at=i.get('ExpiresAt', None)) for i in all_identity_data)

        # Prepare bulk create tuple to save all Scan objects
        scan_bulk_create = (Scan(id=i['ID'],
                                 identity_id=i['IdentityID'],
                                 user_id=i['UserID'],
                                 flags=i['Flags'],
                                 verdict_type=i['VerdictType'],
                                 verdict_result=i['VerdictResult'],
                                 verdict_name=i['VerdictName'],
                                 verdict_value=i['VerdictValue']) for i in all_data)

        # Delete all data from database
        await sync_to_async(delete_data)()

        # Save all data to database
        await Identity.objects.abulk_create(identity_bulk_create)
        await Scan.objects.abulk_create(scan_bulk_create)

        return 'Data generated'


@shared_task()
def populate_data():
    asyncio.run(generate_data())