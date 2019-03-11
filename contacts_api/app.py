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
    return jsonify({'contacts': contacts})

# Return a single contact by its id
@app.route('/contacts/<int:id>', methods=['GET'])
def get_contact(id):
    contact = list(filter(lambda contact: contact['id'] == id, contacts))
    if len(contact) == 0:
        error_message = {'error': 'Contact not found.'}
        return make_response(jsonify(error_message), 404)
    else:
        return jsonify({'contact': contact[0]})

# Create a new Contact
@app.route('/contacts', methods=['POST'])
def create_contact():
    
    if not request.json:
        error_message = {'error': 'Bad request. You must supply data in json format.'}
        return make_response(jsonify(error_message), 400)

    if not contacts:
        new_contact = {
            'id': 1,
        }
    else:
        new_contact = {
            'id': contacts[-1]['id'] + 1
        }

    required_field = 'first_name'
    if not required_field in request.json:
        error_message = {'error': 'Bad request. You must supply at least a first name.'}
        return make_response(jsonify(error_message), 400)

    if not request.json[required_field].strip():
        error_message = {'error': 'Bad request. You supplied an empty first name.'}
        return make_response(jsonify(error_message), 400)

    new_contact['first_name'] = request.json['first_name']
    
    if 'last_name' in request.json:
        new_contact['last_name'] = request.json['last_name']
    else:
        new_contact['last_name'] = ""

    if 'phone_number' in request.json:
        if isinstance(request.json['phone_number'], str) and request.json['phone_number'].isalpha():
            error_message = {'error': 'Bad request. The phone number you provided contains letters.'}
            return make_response(jsonify(error_message), 400)

        new_contact['phone_number'] = request.json['phone_number']
    else:
        new_contact['phone_number'] = ""

    if 'address' in request.json:
        new_contact['address'] = request.json['address']
    else:
        new_contact['address'] = ""

    if 'email' in request.json:
        email_regex = re.compile(r'[\w\.-]+@[\w\.-]+')
        if not email_regex.search(request.json['email']):
            error_message = {'error': 'Bad request. Invalid email address.'}
            return make_response(jsonify(error_message), 400)

        new_contact['email'] = request.json['email']
    else:
        new_contact['email'] = ""

    contacts.append(new_contact)
    return jsonify({'contact': new_contact}), 201






























