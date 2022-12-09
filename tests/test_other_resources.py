import requests
from variables import BASEURL


def test_other_resources():
    '''
    Steps:
    1) Fetch other resources via GET request
    2) process the data received
    '''
    response = requests.get(BASEURL + f'/api/unknow/')
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
