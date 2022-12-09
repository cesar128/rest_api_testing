import requests
from variables import BASEURL

def test_login_successful():
    '''
    Steps:
    1) Simulate a user login sending login details via POST request
    2) process the data received
    '''
    req_body = {
        "email": "eve.holt@reqres.in",
        "password": "pistol"
    }
    response = requests.post(BASEURL + f'/api/login/', json=req_body)
    body = response.json()
    # Response status code for a post request, should be 201, but in this case, this endpoint returns a 200
    assert response.status_code == 200
    # there must be a token in the response
    assert "token" in body
    # token should not be null
    assert body["token"] != None


def test_login_unsuccessful():
    '''
    Steps:
    1) Send a login request via POST, designed and expeted to fail
    2) process the data received
    '''
    req_body = {
        "email": "peter@klaven",
    }
    response = requests.post(BASEURL + f'/api/login/', json=req_body)
    body = response.json()
    # We are waiting it to fail, response status should be 400
    assert response.status_code == 400
    # Making sure we get an error in the body
    assert "error" in body
    # and asserting that the error is not None
    assert body["error"] != None
