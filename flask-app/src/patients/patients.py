from flask import Blueprint, request, jsonify, make_response
import json
from src import db

patients = Blueprint('patient', __name__)

# Get a patient's cancer type id
@patients.route('/user/<first_name>/<last_name>', methods=['GET'])
def get_user_cancer_type(first_name, last_name):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT ct.name, u.cancer_type_id FROM user u JOIN cancer_type ct ON u.cancer_type_id = ct.cancer_type_id WHERE first_name = %s AND last_name = %s', (first_name, last_name))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Add a patient's information
@patients.route('/user', methods=['POST'])
def create_user():
    # Get the request body
    user_data = request.get_json()

    # Extract the necessary fields
    first_name = user_data.get('first_name')
    last_name = user_data.get('last_name')
    cancer_type_id = user_data.get('cancer_type_id')
    occupation = user_data.get('occupation')
    birth_date = user_data.get('birth_date')
    gender = user_data.get('gender')
    city = user_data.get('city')
    state = user_data.get('state')
    email_1 = user_data.get('email_1')
    phone_1 = user_data.get('phone_1')

    # Insert the new information into the database
    cursor = db.get_db().cursor()
    cursor.execute('INSERT INTO user (first_name, last_name, cancer_type_id, occupation, birth_date, gender, city, state, email_1, phone_1) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                   (first_name, last_name, cancer_type_id, occupation, birth_date, gender, city, state, email_1, phone_1))
    db.get_db().commit()

    # Return a success message
    response = make_response(jsonify({'message': 'User created successfully'}))
    response.status_code = 201
    response.mimetype = 'application/json'
    return response

# Delete a patient by id
@patients.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM user WHERE user_id = {0}'.format(user_id))
    user = cursor.fetchone()
    if user:
        cursor.execute('DELETE FROM user WHERE user_id = {0}'.format(user_id))
        db.get_db().commit()
        the_response = make_response(jsonify({'message': 'User has been deleted.'}))
        the_response.status_code = 200
        the_response.mimetype = 'application/json'
    else:
        the_response = make_response(jsonify({'message': 'User not found.'}))
        the_response.status_code = 404
        the_response.mimetype = 'application/json'
    return the_response

# Get patients with specified cancer type ID
@patients.route('/user/<cancer_type_id>', methods=['GET'])
def get_users_by_cancer_type(cancer_type_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM user WHERE cancer_type_id = {0}'.format(cancer_type_id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get all treatments typically used for a given cancer type
@patients.route('/treatment/<cancer_type_id>', methods=['GET'])
def treatment(cancer_type_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT t.treatment_id, t.name FROM treatment t JOIN typically_treated_with tt ON t.treatment_id = tt.treatment_id WHERE tt.cancer_type_id = {0}'.format(cancer_type_id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get all members of a support group
@patients.route('/support_group/<support_group_id>/members', methods=['GET'])
def get_support_group_members(support_group_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT u.user_id, u.first_name, u.last_name FROM user u JOIN member_of m ON u.user_id = m.user_id WHERE m.support_group_id = {0}'.format(support_group_id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Get patients by cancer type and support group (see which groups may have certain cancer types)
@patients.route('/support_group/<support_group_id>/cancer_type/<cancer_type_id>/users', methods=['GET'])
def get_users_by_support_group_and_cancer_type(support_group_id, cancer_type_id):
    cursor = db.get_db().cursor()
    cursor.execute('SELECT u.user_id, u.first_name, u.last_name FROM user u JOIN member_of m ON u.user_id = m.user_id WHERE m.support_group_id = {0} AND u.cancer_type_id = {1}'.format(support_group_id, cancer_type_id))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Update a patient's symptoms
@patients.route('/exhibits/<user_id>', methods=['PUT'])
def update_symptoms(user_id):
    data = request.get_json()
    symptom_id = data.get('symptom_id')
    start_date = data.get('start_date')

    cursor = db.get_db().cursor()
    cursor.execute('UPDATE exhibits SET symptom_id = %s, start_date = %s WHERE user_id = %s', (symptom_id, start_date, user_id))
    db.get_db().commit()

    response = jsonify({'message': 'Added symptom {} to user {}, which started on {}'.format(symptom_id, user_id, start_date)})
    response.status_code = 200
    response.mimetype = 'application/json'
    return response