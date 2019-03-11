import contacts_api.app
import pytest

@pytest.fixture
def app():
      return contacts_api.app.app.test_client()

def test_get_contacts(app):
    test_contacts = {"contacts": contacts_api.app.contacts}

    content_type_header = "application/json"

    response = app.get('/contacts')

    assert response.status_code == 200  
    assert content_type_header in response.headers.get("content-type")
    assert response.is_json
    assert test_contacts == response.get_json()
