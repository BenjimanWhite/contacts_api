# contacts_api
A simple web api written in the flask python microframework for managing a list of contacts.

This api is organized around [REST](https://en.wikipedia.org/wiki/Representational_state_transfer). It has predictable resource-oriented URLs, uses/returns JSON encoded bodies, and implements standard HTTP response codes, verbs, and Basic Authentication.

#### Installation for development
Clone this repository:
`$ git clone git@github.com:BenjimanWhite/contacts_api.git`

Create a virtual environment in the root of the project directory:
`$ python -m venv venv`

Activate the virtual environment:
`$ source bin/venv/activate`

Install dependencies and set up the application:
`pip install .`

#### Using in development
To run the flask app execute the following command in the root of the project:
`$ FLASK_APP=contacts_api.app flask run`

This application uses pytest. To run its tests execute in the root of the project:
`pytest tests/`

### Base URL
The base url for local development is `http://localhost:5000`

### Authentication
HTTP Basic Authentication is required to modify data (contact creation, updating, deletion). Because this is a simple api meant for local development only at the moment, you can use the following credentials to authenticate:
username - benjiman
password - supersecretpass

Make sure to correctly format and encode these credentials into base64 so they are accepted as required by the [Basic Auth specification](https://tools.ietf.org/html/rfc7617).

#### Contact Resource
A *contact* is the main object of this application. It keeps track of the following attributes:
___
*address* - A string representing a contact's address. Set to an empty string if not specifed when a contact is created.
___
*email* - A string representing a contacts's email address. Set to an empty string if not specified when a contact is created. Will return a HTTP `400` if the email fails basic validation. 
___
*first_name* - A string representing a contact's first name. This is the only required field when creating or updating a contact; forgetting to include it will return a HTTP `400` error.
___
*last_name* - A string representing a contact's last name. Set to an empty string if not specified when a contact is created.
___
*phone_number* - Either a string or integer representation for a contact's phone number. Set to an empty string if not specified when a contact is created. Will return a HTTP `400` if the supplied string contains letters upon creation or update.

### Examples

Return a list of contacts:
``` GET localhost:5000/contacts```
___
Return a list of contacts, filtering by attribute. Note that only the first attribute passed is processed. The response will return a `400` error code if an unknown attribute is used.
```GET localhost:5000/contacts?email=ada@computingrocks.net```
___
Create a new contact. Note that this requires the authorization header described under Authentication above.
```
example_new_contact = {
  "first_name": "Bill",
  "last_name": "Hamilton",
  "phone_number": "6175557834",
  "address": "17 Inman St. Cambridge, MA 02139, USA",
  "email": "bill@anotherplace.com"
}
```

`POST example_new_contact correct_auth_headers localhost:5000/contacts`
___
Update an existing contact. Note that this requires the authorization header described under Authentication above.
```
example_updated_contact = {
  "first_name": "William",
  "last_name": "Hamiltonian",
  "id": 4,
  "last_modified_by": 'benjiman'
}
```

```PUT example_updated_contact localhost:5000/contacts/4```
___
Delete a contact. Note that this requires the authorization header described under Authentication above.
```DELETE localhost:5000/contacts/4```

































