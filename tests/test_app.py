import contacts_api.app
import pytest

@pytest.fixture
def app():
      return contacts_api.app.app.test_client()

def test_get_contacts(app):
    test_contacts = {"contacts": contacts_api.app.contacts}

    json_header = "application/json"

    response = app.get('/contacts')

    assert response.status_code == 200  
    assert json_header in response.headers.get("content-type")
    assert test_contacts == response.get_json()

def test_get_contact(app):

    # Test happiest path
    test_contact = contacts_api.app.contacts[0]

    json_header = "application/json"

    response = app.get('/contacts/1')

    assert response.status_code == 200  
    assert json_header in response.headers.get("content-type")
    assert test_contact == response.get_json()

    # Test - unknown contact SHOULD return 404 not found 

def test_create_contact(app):
    valid_new_contact = {
        "first_name": "Bell",
        "last_name": "Hooks",
        "address": "300 Center St. Berea KY 40403 USA",
        "phone_number": "(859) 985 - 2878",
        "email": "bell@changingtheworld.edu"
    }
    json_header = "application/json"

    # Test happiest path
    response = app.post('/contacts', json=valid_new_contact)

    valid_new_contact['id'] = 3

    assert response.status_code == 201  
    assert json_header in response.headers.get("content-type")
    assert valid_new_contact == response.get_json()

    del valid_new_contact['id']

    # Test that id is properly set if our contacts list is empty TODO

    # Test bad json passed in TODO
    # not_json = "<first_name> Bell </first_name>"
    # response = app.post('/contacts', json=not_json)
    
    # assert response.status_code == 400
    # assert response.get_json == {'error': 'Bad request. You must supply data in json format.'}

    # Test - unspecified fields are assigned to ''
    only_first_name_contact = {"first_name": "Miriam"}
    expected_result = {
        'id': 4,
        'first_name': 'Miriam',
        'last_name': '',
        'phone_number': '',
        'address': '',
        'email': ''
    }

    response = app.post('/contacts', json=only_first_name_contact)

    assert response.status_code == 201  
    assert json_header in response.headers.get("content-type")
    assert response.get_json() == expected_result

    # Test - first name MUST BE present
    no_first_name_contact = valid_new_contact.copy()
    del no_first_name_contact['first_name']
    error = {'error': 'Bad request. You must supply at least a first name.'}

    response = app.post('/contacts', json=no_first_name_contact)

    assert response.status_code == 400  
    assert json_header in response.headers.get("content-type")
    assert response.get_json() == error

    # Test - first name SHOULD NOT BE empty
    empty_first_name_contact = valid_new_contact.copy()
    empty_first_name_contact['first_name'] = ""
    error = {'error': 'Bad request. You supplied an empty first name.'}

    response = app.post('/contacts', json=empty_first_name_contact)

    assert response.status_code == 400  
    assert json_header in response.headers.get("content-type")
    assert response.get_json() == error

    # Test - phone number SHOULD NOT HAVE letters
    alphabetical_phone_number_contact = valid_new_contact.copy()
    alphabetical_phone_number_contact['phone_number'] = "my number is (503) - 654 - 5543"
    error = {'error': 'Bad request. The phone number you provided contains letters.'}

    response = app.post('/contacts', json=alphabetical_phone_number_contact)
    
    assert response.status_code == 400  
    assert json_header in response.headers.get("content-type")
    assert response.get_json() == error

    # Test email address SHOULD BE valid

    invalid_email_contact = valid_new_contact.copy()
    invalid_email_contact['email'] = "emailatsomethingdotedu"

    error = {'error': 'Bad request. Invalid email address.'}

    response = app.post('/contacts', json=invalid_email_contact)
    assert response.status_code == 400  
    assert json_header in response.headers.get("content-type")
    assert response.get_json() == error
















    

























