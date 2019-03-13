import contacts_api.app
import pytest

@pytest.fixture
def app():
      return contacts_api.app.app.test_client()


def test_get_contacts(app):
    # Test - getting all contacts
    test_contacts = {"contacts": contacts_api.app.contacts}
    json_header = "application/json"
    response = app.get('/contacts')
    assert response.status_code == 200  
    assert json_header in response.headers.get("content-type")
    assert test_contacts == response.get_json()

    # Test - searching by query parameters
    test_contact = contacts_api.app.contacts[0]
    query_key = 'email'
    query_value = test_contact['email']
    response = app.get(f"/contacts?{query_key}={query_value}")
    assert response.status_code == 200  
    assert json_header in response.headers.get("content-type")
    assert {'contacts': [test_contact]} == response.get_json()


def test_get_contact(app):
    # Test happiest path
    test_contact = contacts_api.app.contacts[0]
    contact_id = test_contact['id']
    json_header = "application/json"
    response = app.get(f"/contacts/{contact_id}")
    assert response.status_code == 200  
    assert json_header in response.headers.get("content-type")
    assert test_contact == response.get_json()

    # Test - unknown contact SHOULD return 404 not found
    response = app.get('/contacts/10')
    assert response.status_code == 404

def test_create_contact(app):
    valid_auth_header = {'Authorization': 'Basic YmVuamltYW46c3VwZXJzZWNyZXRwYXNz'}

    # Test happiest path
    valid_new_contact = {
        'first_name': 'Bell',
        'last_name': 'Hooks',
        'address': '300 Center St. Berea KY 40403 USA',
        'phone_number': '(859) 985 - 2878',
        'email': 'bell@changingtheworld.edu',
        'uri': 'http://localhost/contacts/3'
    }
    json_header = "application/json"
    response = app.post('/contacts', headers=valid_auth_header, json=valid_new_contact)
    #valid_new_contact['id'] = 3
    valid_new_contact['last_modified_by'] = 'benjiman'
    assert response.status_code == 201
    assert json_header in response.headers.get("content-type")
    assert valid_new_contact == response.get_json()
    #del valid_new_contact['id']

    # Test bad json passed in
    xml = "<first_name> Bell </first_name>"
    response = app.post('/contacts', headers=valid_auth_header, data=xml)
    assert response.status_code == 400
    
    # Test - unspecified fields are assigned to ''
    only_first_name_contact = {"first_name": "Miriam"}
    expected_result = {
        'first_name': 'Miriam',
        'last_name': '',
        'phone_number': '',
        'address': '',
        'email': '',
        'last_modified_by': 'benjiman',
        'uri': 'http://localhost/contacts/4'
    }
    response = app.post('/contacts', headers=valid_auth_header, json=only_first_name_contact)
    assert response.status_code == 201  
    assert json_header in response.headers.get("content-type")
    assert response.get_json() == expected_result

    #################### first name ##############################
    # Test - first name MUST BE present
    no_first_name_contact = valid_new_contact.copy()
    del no_first_name_contact['first_name']
    error = {'error': 'Bad request. You must supply at least a first name.'}
    response = app.post('/contacts', headers=valid_auth_header, json=no_first_name_contact)
    assert response.status_code == 400  
    assert json_header in response.headers.get("content-type")
    assert response.get_json() == error

    # Test - first name SHOULD BE a string
    non_string_first_name_contact = valid_new_contact.copy()
    non_string_first_name_contact['first_name'] = 9715007864
    error = {'error': 'Bad request. First name must be a string.'}
    response = app.post('/contacts', headers=valid_auth_header, json=non_string_first_name_contact)
    assert response.status_code == 400  
    assert json_header in response.headers.get("content-type")
    assert response.get_json() == error

    # Test - first name SHOULD NOT BE empty
    empty_first_name_contact = valid_new_contact.copy()
    empty_first_name_contact['first_name'] = ""
    error = {'error': 'Bad request. You supplied an empty first name.'}
    response = app.post('/contacts', headers=valid_auth_header, json=empty_first_name_contact)
    assert response.status_code == 400  
    assert json_header in response.headers.get("content-type")
    assert response.get_json() == error

    ###################### last name #############################
    # Test - last name SHOULD BE a string
    non_string_last_name_contact = valid_new_contact.copy()
    non_string_last_name_contact['last_name'] = 9715007864
    error = {'error': 'Bad request. Last name must be a string.'}
    response = app.post('/contacts', headers=valid_auth_header, json=non_string_last_name_contact)
    assert response.status_code == 400
    assert json_header in response.headers.get("content-type")
    assert response.get_json() == error

    ####################### phone number #########################
    # Test - phone number MUST BE an integer if it is not a string
    invalid_phone_number_contact = valid_new_contact.copy()
    invalid_phone_number_contact['phone_number'] = {"phone_number": 5045567489}
    error = {'error': 'Bad request. The phone number must be an integer if it is not a string.'}
    response = app.post('/contacts', headers=valid_auth_header, json=invalid_phone_number_contact)
    assert response.status_code == 400  
    assert json_header in response.headers.get("content-type")
    assert response.get_json() == error

    # Test - phone number SHOULD NOT HAVE letters
    alphabetical_phone_number_contact = valid_new_contact.copy()
    alphabetical_phone_number_contact['phone_number'] = "my number is (503) - 654 - 5543"
    error = {'error': 'Bad request. The phone number you provided contains letters.'}
    response = app.post('/contacts', headers=valid_auth_header, json=alphabetical_phone_number_contact)  
    assert response.status_code == 400  
    assert json_header in response.headers.get("content-type")
    assert response.get_json() == error

    ##################### address ################################
    # Test - address SHOULD BE a string
    non_string_address_contact = valid_new_contact.copy()
    non_string_address_contact['address'] = 9715007864
    error = {'error': 'Bad request. Address must be a string.'}
    response = app.post('/contacts', headers=valid_auth_header, json=non_string_address_contact)
    assert response.status_code == 400
    assert json_header in response.headers.get("content-type")
    assert response.get_json() == error

    
    ################### email ####################################
    # Test - email SHOULD BE a string
    non_string_email_contact = valid_new_contact.copy()
    non_string_email_contact['email'] = 9715007864
    error = {'error': 'Bad request. Email must be a string.'}
    response = app.post('/contacts', headers=valid_auth_header, json=non_string_email_contact)
    assert response.status_code == 400
    assert json_header in response.headers.get("content-type")
    assert response.get_json() == error

    # Test email address SHOULD BE valid
    invalid_email_contact = valid_new_contact.copy()
    invalid_email_contact['email'] = "emailatsomethingdotedu"
    error = {'error': 'Bad request. Invalid email address.'}
    response = app.post('/contacts', headers=valid_auth_header, json=invalid_email_contact)
    assert response.status_code == 400  
    assert json_header in response.headers.get("content-type")
    assert response.get_json() == error

    # Test - no auth headers provided
    error = {'error': 'Forbidden. You must authenticate to access this.'}
    response = app.post('/contacts', json=valid_new_contact)
    assert response.status_code == 401
    assert response.get_json() == error

    # Test - invalid username provided
    invalid_username_auth_header = {'Authorization': 'Basic Ym9vZ2V5bWFuOnN1cGVyc2VjcmV0cGFzcw=='}
    error = {'error': 'Forbidden. Please supply a valid username.'}
    response = app.post('/contacts', headers=invalid_username_auth_header, json=valid_new_contact)
    assert response.status_code == 401
    assert response.get_json() == error

    # Test - invalid password provided
    invalid_password_auth_header = {'Authorization': 'Basic YmVuamltYW46c3VwZXJzZWNyZXRwYSQk'}
    error = {'error': 'Forbidden. Please supply a valid password.'}
    response = app.post('/contacts', headers=invalid_password_auth_header, json=valid_new_contact)
    assert response.status_code == 401
    assert response.get_json() == error

    # Test that new contact id is set properly when contacts list becomes empty
    app.delete(f"/contacts/1", headers=valid_auth_header)
    app.delete(f"/contacts/2", headers=valid_auth_header)
    app.delete(f"/contacts/3", headers=valid_auth_header)
    app.delete(f"/contacts/4", headers=valid_auth_header)
    response = app.post('/contacts', headers=valid_auth_header, json=valid_new_contact)
    valid_new_contact['last_modified_by'] = 'benjiman'
    valid_new_contact['uri'] = 'http://localhost/contacts/1'
    assert response.status_code == 201
    assert json_header in response.headers.get("content-type")
    assert valid_new_contact == response.get_json()

def test_update_contact(app):
    valid_auth_header = {'Authorization': 'Basic YmVuamltYW46c3VwZXJzZWNyZXRwYXNz'}

    json_header = 'application/json'
    original_contact = contacts_api.app.contacts[0]

    # Test happiest path
    contact_id = original_contact['id']
    updated_contact = {
        'id': contact_id,
        'first_name': 'Radia',
        'last_name': 'Perlman',
        'phone_number': '7863043389',
        'address': '345 Somewhere Ln. Portsmouth, VA 97878 USA',
        'email': 'erlmanp@somewhere.org',
        'uri': f"http://localhost/contacts/{contact_id}",
        'last_modified_by': 'benjiman'
    }
    response = app.put(f"/contacts/{contact_id}", headers=valid_auth_header, json=updated_contact)
    assert response.status_code == 200
    assert json_header in response.headers.get("content-type")
    assert updated_contact == response.get_json()
    
    # Test - unknown contact id SHOULD return 404 not found
    response = app.put('/contacts/10', headers=valid_auth_header, json=updated_contact)
    error = {'error': 'Contact not found.'}
    assert response.status_code == 404
    assert response.get_json() == error

    # Test bad json passed in
    xml = "<first_name> Bell </first_name>"
    response = app.put(f"/contacts/{contact_id}", headers=valid_auth_header, data=xml)
    assert response.status_code == 400

    #################### first name ##############################
    # Test - first name SHOULD BE a string
    invalid_first_name_contact = original_contact.copy()
    invalid_first_name_contact['first_name'] = 9715007864
    error = {'error': 'Bad request. First name must be a string.'}
    response = app.put(f"/contacts/{contact_id}", headers=valid_auth_header, json=invalid_first_name_contact)
    assert response.status_code == 400  
    assert json_header in response.headers.get("content-type")
    assert response.get_json() == error

    # Test - first name SHOULD NOT BE empty
    empty_first_name_contact = original_contact.copy()
    empty_first_name_contact['first_name'] = ""
    error = {'error': 'Bad request. You supplied an empty first name.'}
    response = app.put(f"/contacts/{contact_id}", headers=valid_auth_header, json=empty_first_name_contact)
    assert response.status_code == 400  
    assert json_header in response.headers.get("content-type")
    assert response.get_json() == error

    ###################### last name #############################
    # Test - last name SHOULD BE a string
    invalid_last_name_contact = original_contact.copy()
    invalid_last_name_contact['last_name'] = 9715007864
    error = {'error': 'Bad request. Last name must be a string.'}
    response = app.put(f"/contacts/{contact_id}", headers=valid_auth_header, json=invalid_last_name_contact)
    assert response.status_code == 400
    assert json_header in response.headers.get("content-type")
    assert response.get_json() == error

    ####################### phone number #########################
    # Test - phone number MUST BE an integer if it is not a string
    invalid_phone_number_contact = original_contact.copy()
    invalid_phone_number_contact['phone_number'] = {"phone_number": 5045567489}
    error = {'error': 'Bad request. The phone number must be an integer if it is not a string.'}
    response = app.put(f"/contacts/{contact_id}", headers=valid_auth_header, json=invalid_phone_number_contact)
    assert response.status_code == 400
    assert json_header in response.headers.get("content-type")
    assert response.get_json() == error

    # Test - phone number SHOULD NOT HAVE letters
    alphabetical_phone_number_contact = original_contact.copy()
    alphabetical_phone_number_contact['phone_number'] = "my number is (503) - 654 - 5543"
    error = {'error': 'Bad request. The phone number you provided contains letters.'}
    response = app.put(f"/contacts/{contact_id}", headers=valid_auth_header, json=alphabetical_phone_number_contact)
    assert response.status_code == 400  
    assert json_header in response.headers.get("content-type")
    assert response.get_json() == error

    ##################### address ################################
    # Test - address SHOULD BE a string
    non_string_address_contact = original_contact.copy()
    non_string_address_contact['address'] = 9715007864
    error = {'error': 'Bad request. Address must be a string.'}
    response = app.put(f"/contacts/{contact_id}", headers=valid_auth_header, json=non_string_address_contact)
    assert response.status_code == 400
    assert json_header in response.headers.get("content-type")
    assert response.get_json() == error
    
    ################### email ####################################
    # Test - email SHOULD BE a string
    non_string_email_contact = original_contact.copy()
    non_string_email_contact['email'] = 9715007864
    error = {'error': 'Bad request. Email must be a string.'}
    response = app.put(f"/contacts/{contact_id}", headers=valid_auth_header, json=non_string_email_contact)
    assert response.status_code == 400
    assert json_header in response.headers.get("content-type")
    assert response.get_json() == error

    # Test email address SHOULD BE valid
    invalid_email_contact = original_contact.copy()
    invalid_email_contact['email'] = "emailatsomethingdotedu"
    error = {'error': 'Bad request. Invalid email address.'}
    response = app.put(f"/contacts/{contact_id}", headers=valid_auth_header, json=invalid_email_contact)
    assert response.status_code == 400  
    assert json_header in response.headers.get("content-type")
    assert response.get_json() == error

    # Test - no auth headers provided
    error = {'error': 'Forbidden. You must authenticate to access this.'}
    response = app.put(f"/contacts/{contact_id}", json=updated_contact)
    assert response.status_code == 401
    assert response.get_json() == error

    # Test - invalid username provided
    invalid_username_auth_header = {'Authorization': 'Basic Ym9vZ2V5bWFuOnN1cGVyc2VjcmV0cGFzcw=='}
    error = {'error': 'Forbidden. Please supply a valid username.'}
    response = app.put(f"/contacts/{contact_id}", headers=invalid_username_auth_header, json=updated_contact)
    assert response.status_code == 401
    assert response.get_json() == error

    # Test - invalid password provided
    invalid_password_auth_header = {'Authorization': 'Basic YmVuamltYW46c3VwZXJzZWNyZXRwYSQk'}
    error = {'error': 'Forbidden. Please supply a valid password.'}
    response = app.put(f"/contacts/{contact_id}", headers=invalid_password_auth_header, json=updated_contact)
    assert response.status_code == 401
    assert response.get_json() == error

def test_delete_contact(app): 
    valid_auth_header = {'Authorization': 'Basic YmVuamltYW46c3VwZXJzZWNyZXRwYXNz'}
    contact = contacts_api.app.contacts[0]
    contact_id = contact['id']

    # Test - unknown contact id SHOULD return 404 not found
    response = app.delete('/contacts/10', headers=valid_auth_header)
    error = {'error': 'Contact not found.'}
    assert response.status_code == 404
    assert response.get_json() == error

    # Test - delete is successful
    success = {'result': 'contact deleted.'}
    response = app.delete(f"/contacts/{contact_id}", headers=valid_auth_header)
    assert response.status_code == 200  
    assert 'application/json' in response.headers.get("content-type")
    assert success == response.get_json()

    # Test - no auth headers provided
    error = {'error': 'Forbidden. You must authenticate to access this.'}
    response = app.delete(f"/contacts/{contact_id}")
    assert response.status_code == 401
    assert response.get_json() == error

    # Test - invalid username provided
    invalid_username_auth_header = {'Authorization': 'Basic Ym9vZ2V5bWFuOnN1cGVyc2VjcmV0cGFzcw=='}
    error = {'error': 'Forbidden. Please supply a valid username.'}
    response = app.delete(f"/contacts/{contact_id}", headers=invalid_username_auth_header)
    assert response.status_code == 401
    assert response.get_json() == error

    # Test - invalid password provided
    invalid_password_auth_header = {'Authorization': 'Basic YmVuamltYW46c3VwZXJzZWNyZXRwYSQk'}
    error = {'error': 'Forbidden. Please supply a valid password.'}
    response = app.delete(f"/contacts/{contact_id}", headers=invalid_password_auth_header)
    assert response.status_code == 401
    assert response.get_json() == error
