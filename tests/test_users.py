import requests
from variables import BASEURL

def test_list_users(page=2):
    '''
    Steps:
    1) Request the data via GET
    2) process the data list
    '''
    response = requests.get(BASEURL + f'/api/users/?page={page}')
    body = response.json()

    # Response status for a get request should be 200
    assert response.status_code == 200
    # Response data must be a list
    assert type(body['data']) == list
        # Page should be a non-zero positive number
    assert body['page'] > 0

    # The amount of result returned should correspond to the page we are requesting
    if body['page'] > body['total_pages']:
        # if the current page is greater than total pages, array length should be empty
        expected_length = 0
    elif body['page'] < body['total_pages']:
        # if the current page is less than total pages, we should have the whole results per page
        expected_length = body['per_page']
    else:
        # if we are in the last page, length of the result data should be `total` results minus `(page - 1) * per_page`
        expected_length = body['total'] - \
            ((body['total_pages'] - 1) * body['per_page'])

    assert len(body['data']) == expected_length


def test_create_user():
    '''
    Steps:
    1) Request the data via POST
    2) process the data received
    '''
    req_body = {"name": "morpheus", "job": "leader"}
    response = requests.post(BASEURL + f'/api/users/', json=req_body)
    body = response.json()
    # Response status code for a post request, should be 201
    assert response.status_code == 201
    # Ignoring capitalization, name and job should be the same.
    assert req_body['name'].lower() == body['name'].lower(
    ) and req_body['job'].lower() == body['job'].lower()
    # Created object must have an id and that id shoud not be None/null
    assert 'id' in body and body['id'] is not None


def test_put_user(user_id=2):
    '''
    Steps:
    1) Change user data via PUT
    2) test the data received
    '''
    import datetime
    local_updated_at = datetime.datetime.utcnow()

    req_body = {"name": "morpheus", "job": "zion resident"}
    response = requests.put(BASEURL + f'/api/users/{user_id}', json=req_body)
    body = response.json()

    # Response status code for a put request, should be 200
    assert response.status_code == 200
    # Ignoring capitalization, name and job should be the same.
    assert req_body['name'].lower() == body['name'].lower(
    ) and req_body['job'].lower() == body['job'].lower()

    # Asserting local_updated_at and response updated_at time difference is below 10 secs
    remote_updated_at = datetime.datetime.strptime(
        body['updatedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
    assert (remote_updated_at - local_updated_at).total_seconds() < 10
    pass


def test_patch_user(user_id=2):
    '''
    Steps:
    1) change some information of the user via PATCH 
    2) process the data received
    '''
    import datetime
    local_updated_at = datetime.datetime.utcnow()

    req_body = {"name": "morpheus", "job": "zion resident"}
    response = requests.patch(BASEURL + f'/api/users/{user_id}', json=req_body)
    body = response.json()

    # Response status code for a put request, should be 200
    assert response.status_code == 200
    # Ignoring capitalization, name and job should be the same.
    assert req_body['name'].lower() == body['name'].lower(
    ) and req_body['job'].lower() == body['job'].lower()

    # Asserting local_updated_at and response updated_at time difference is below 10 secs
    remote_updated_at = datetime.datetime.strptime(
        body['updatedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
    assert (remote_updated_at - local_updated_at).total_seconds() < 10
    pass


def test_delete_user(user_id=2):
    '''
    Steps:
    1) Send a request to delete one user via DELETE method
    2) process the data received
    '''
    response = requests.delete(BASEURL + f'/api/users/{user_id}')

    # Response status for a get request should be 200
    assert response.status_code == 204

