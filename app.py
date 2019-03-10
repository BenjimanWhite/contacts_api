from flask import Flask, jsonify
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
