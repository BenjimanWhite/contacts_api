from flask import Flask, jsonify, abort, make_response
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
        abort(404)
    else:
        return jsonify({'contact': contact[0]})

@app.errorhandler(404)
def not_found(error):
  message = {'error': 'Contact not found'}
  return make_response(jsonify(message), 404)