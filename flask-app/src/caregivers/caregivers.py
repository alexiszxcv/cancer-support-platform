from flask import Blueprint, request, jsonify, make_response
import json
from src import db

caregivers = Blueprint('caregiver', __name__)

# Get all caregiver user ids and names
@caregivers.route('/user', methods=['GET'])
def get_user():
    user_id = request.args.get('user_id')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT user_id, first_name, last_name FROM user')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Update caregiver contact info
@caregivers.route('/user/<int:user_id>', methods=['PUT'])
def update_user_caregiver(user_id):
    data = request.get_json()
    email_1 = data.get('email_1')
    email_2 = data.get('email_2')
    phone_1 = data.get('phone_1')
    phone_2 = data.get('phone_2')
    cursor = db.get_db().cursor()
    cursor.execute('UPDATE user SET email_1 = %s, email_2 = %s, phone_1 = %s, phone_2 = %s WHERE user_id = %s', (email_1, email_2, phone_1, phone_2, user_id))
    db.get_db().commit()

    return jsonify(message='Caregiver updated successfully!')

# Delete a caregiver
@caregivers.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user_caregiver(user_id):
    # Connect to the database
    db_conn = db.get_db()
    cursor = db_conn.cursor()

    # Delete the user from the "member_of" table
    cursor.execute('DELETE FROM member_of WHERE user_id = %s', (user_id,))
    db_conn.commit()

    # Delete the user from the "exhibits" table
    cursor.execute('DELETE FROM exhibits WHERE user_id = %s', (user_id,))
    db_conn.commit()

    # Delete the user from the "supported_by" table
    cursor.execute('DELETE FROM supported_by WHERE user_id = %s', (user_id,))
    db_conn.commit()

    # Delete the user from the "user" table
    cursor.execute('DELETE FROM user WHERE user_id = %s', (user_id,))
    db_conn.commit()

    return jsonify(message='Caregiver deleted successfully!')

# Add a medical professional
@caregivers.route('/medical-professionals/add', methods=['POST'])
def add_medical_professional():
    # Get the request body
    medical_professional_data = request.get_json()

    # Extract the necessary fields
    first_name = medical_professional_data.get('first_name')
    last_name = medical_professional_data.get('last_name')
    specialty = medical_professional_data.get('specialty')
    treatment_id = medical_professional_data.get('treatment')

    # insert a new row into the database with the new professional's data
    cursor = db.get_db().cursor()
    cursor.execute('INSERT INTO medical_professional (first_name, last_name, specialty, treatment_id) VALUES (%s, %s, %s, %s)', (first_name, last_name, specialty, treatment_id))

    # return success message
    return 'New medical professional added successfully!'

# Get all treatment centers
@caregivers.route('/treatment-centers', methods=['GET'])
def get_treatment_centers():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT center_id, name, street_address, state, city, zip_code, website, professional_id, email_1, email_2, phone_1, phone_2 FROM treatment_center')
    row_headers = [x[0] for x in cursor.description]
    center_list = []
    theData = cursor.fetchall()
    for row in theData:
        center_list.append(dict(zip(row_headers, row)))
    # return the center_list as JSON
    the_response = make_response(jsonify(center_list))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Get all user connections
@caregivers.route('/connections', methods=['GET'])
def get_connections():
    #user_id = request.args.get('user_id')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT user_id_1, user_id_2, relationship FROM makes_connection')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get all symptom names and ids
@caregivers.route('/symptoms', methods=['GET'])
def get_symptoms():
    cursor = db.get_db().cursor()
    cursor.execute('SELECT symptom_id, name FROM symptom')
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Get medications that treat a given symptom
@caregivers.route('/symptom-treated-with/<symptom_id>', methods=['GET'])
def user_medication(symptom_id):
    #user_id = request.args.get('user_id')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT s.medication_id, name FROM symptom_treated_with s JOIN medication m ON s.medication_id = m.medication_id WHERE symptom_id = %s', symptom_id)
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response