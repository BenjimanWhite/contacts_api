from flask import Flask, jsonify, abort, make_response, request
import re
app = Flask(__name__)

contacts = [
    {
        'id': 1,
        'first_name': 'Margaret',
        'last_name': 'Hamilton',
        'phone_number': '6175557834',
        'address': '17 Inman St. Cambridge, MA 02139, USA',
        'email': 'margaret@hamiltontechnologies.com'
    },
    {
        'id': 2,
        'first_name': 'Ada',
        'last_name': 'Lovelace',
        'phone_number': '4803409032',
        'address': 'Great Russell St, Bloomsbury, London, WC1B 3DG, UK',
        'email': 'ada@computingrocks.net'
    }
]

# Return all contacts
@app.route('/contacts', methods=['GET'])
def get_contacts():
    if request.args:
        query_fields = request.args.items() # query_fields is an iterator of tuples containing query string key=value pairs
        for pair in query_fields:
            key = pair[0]
            value = pair[1]
            if(key == 'first_name'):
                search_results = list(filter(lambda contact: contact[key] == value, contacts))
                return jsonify({'contacts': search_results})
            if(key == 'last_name'):
                search_results = list(filter(lambda contact: contact[key] == value, contacts))
                return jsonify({'contacts': search_results})
            if(key == 'phone_number'):
                search_results = list(filter(lambda contact: contact[key] == value, contacts))
                return jsonify({'contacts': search_results})
            if(key == 'address'):
                search_results = list(filter(lambda contact: contact[key] == value, contacts))
                return jsonify({'contacts': search_results})
            if(key == 'email'):
                search_results = list(filter(lambda contact: contact[key] == value, contacts))
                return jsonify({'contacts': search_results})
        error_message = {'error': 'Bad request. You supplied disallowed query parameters.'}
        return make_response(jsonify(error_message), 400)

    return jsonify({'contacts': contacts})

# Return a single contact by its id
@app.route('/contacts/<int:id>', methods=['GET'])
def get_contact(id):
    contact = list(filter(lambda contact: contact['id'] == id, contacts))
    if len(contact) == 0:
        error_message = {'error': 'Contact not found.'}
        return make_response(jsonify(error_message), 404)
    else:
        return jsonify(contact[0])

# Create a new Contact
@app.route('/contacts', methods=['POST'])
def create_contact():
    
    # Disallow non-json
    if not request.headers['content-type'] == 'application/json':
        abort(400)

    if not contacts:
        new_contact = {
            'id': 1
        }
    else:
        new_contact = {
            'id': contacts[-1]['id'] + 1
        }

    if not 'first_name' in request.json:
        error_message = {'error': 'Bad request. You must supply at least a first name.'}
        return make_response(jsonify(error_message), 400)

    if not isinstance(request.json['first_name'], str):
        error_message = {'error': 'Bad request. First name must be a string.'}
        return make_response(jsonify(error_message), 400)

    if not request.json['first_name'].strip():
        error_message = {'error': 'Bad request. You supplied an empty first name.'}
        return make_response(jsonify(error_message), 400)

    new_contact['first_name'] = request.json['first_name'].strip()
    
    if 'last_name' in request.json:
        if not isinstance(request.json['last_name'], str):
            error_message = {'error': 'Bad request. Last name must be a string.'}
            return make_response(jsonify(error_message), 400)

        new_contact['last_name'] = request.json['last_name'].strip()
    else:
        new_contact['last_name'] = ''

    if 'phone_number' in request.json:
        number = request.json['phone_number']
        alphabetical_chars = '[a-zA-Z]+'
        if isinstance(number, str):
            if re.search(alphabetical_chars, number):
                error_message = {'error': 'Bad request. The phone number you provided contains letters.'}
                return make_response(jsonify(error_message), 400)

            new_contact['phone_number'] = request.json['phone_number'].strip()
        else:
            if not isinstance(number, int):
                error_message = {'error': 'Bad request. The phone number must be an integer if it is not a string.'}
                return make_response(jsonify(error_message), 400)

            new_contact['phone_number'] = request.json['phone_number']
    else:
        new_contact['phone_number'] = ''

    if 'address' in request.json:
        if not isinstance(request.json['address'], str):
            error_message = {'error': 'Bad request. Address must be a string.'}
            return make_response(jsonify(error_message), 400)

        new_contact['address'] = request.json['address'].strip()
    else:
        new_contact['address'] = ''

    if 'email' in request.json:
        if not isinstance(request.json['email'], str):
            error_message = {'error': 'Bad request. Email must be a string.'}
            return make_response(jsonify(error_message), 400)

        email_regex = re.compile(r'[\w\.-]+@[\w\.-]+')
        if not email_regex.search(request.json['email']):
            error_message = {'error': 'Bad request. Invalid email address.'}
            return make_response(jsonify(error_message), 400)

        new_contact['email'] = request.json['email'].strip()
    else:
        new_contact['email'] = ''

    contacts.append(new_contact)
    return jsonify(new_contact), 201

@app.route('/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    contact = list(filter(lambda contact: contact['id'] == id, contacts))

    if len(contact) == 0:
        error_message = {'error': 'Contact not found.'}
        return make_response(jsonify(error_message), 404)

    if not request.headers['content-type'] == 'application/json':
        abort(400)

    if 'first_name' in request.json:
        if not isinstance(request.json['first_name'], str):
            error_message = {'error': 'Bad request. First name must be a string.'}
            return make_response(jsonify(error_message), 400)
        
        if not request.json['first_name'].strip():
            error_message = {'error': 'Bad request. You supplied an empty first name.'}
            return make_response(jsonify(error_message), 400)

        contact[0]['first_name'] = request.json['first_name'].strip()

    if 'last_name' in request.json:
        if not isinstance(request.json['last_name'], str):
            error_message = {'error': 'Bad request. Last name must be a string.'}
            return make_response(jsonify(error_message), 400)

        contact[0]['last_name'] = request.json['last_name'].strip()


    if 'phone_number' in request.json:
        if isinstance(request.json['phone_number'], str):
            alphabetical_chars = '[a-zA-Z]+'
            if re.search(alphabetical_chars, request.json['phone_number']):
                error_message = {'error': 'Bad request. The phone number you provided contains letters.'}
                return make_response(jsonify(error_message), 400)

            contact[0]['phone_number'] = request.json['phone_number'].strip()
        else:
            if not isinstance(request.json['phone_number'], int):
                error_message = {'error': 'Bad request. The phone number must be an integer if it is not a string.'}
                return make_response(jsonify(error_message), 400)

            contact[0]['phone_number'] = request.json['phone_number']

    if 'address' in request.json:
        if not isinstance(request.json['address'], str):
            error_message = {'error': 'Bad request. Address must be a string.'}
            return make_response(jsonify(error_message), 400)

        contact[0]['address'] = request.json['address'].strip()


    if 'email' in request.json:
        if not isinstance(request.json['email'], str):
            error_message = {'error': 'Bad request. Email must be a string.'}
            return make_response(jsonify(error_message), 400)

        email_regex = re.compile(r'[\w\.-]+@[\w\.-]+')
        if not email_regex.search(request.json['email']):
            error_message = {'error': 'Bad request. Invalid email address.'}
            return make_response(jsonify(error_message), 400)

        contact[0]['email'] = request.json['email'].strip()

    return jsonify(contact[0]), 200


@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = list(filter(lambda contact: contact['id'] == id, contacts))
    if len(contact) == 0:
        error_message = {'error': 'Contact not found.'}
        return make_response(jsonify(error_message), 404)

    contacts.remove(contact[0])
    success_message = {'result': 'contact deleted.'}
    return jsonify(success_message), 200

## TODO
# test address fields in create and update
# Add HTTP Basic auth - store reference to the authenticated user in the modified record!
# Test http basic auth
# Add filter functionality by query string
# Test filter Functionality by query string
# document api
# decompose app
# Test distribution on another machine
# send app






















