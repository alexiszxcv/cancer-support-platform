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


# #Add caregiver info
# @caregivers.route('/user', methods=['PUT'])
# def add_user_caregiver():
#     data = request.get_json()
#     first_name = data['first_name']
#     last_name = data['last_name']
#     email = data['email']
#     phone_1 = data['phone_1']
#     city = data['city']
#     state = data['state']
#     cursor = db.get_db().cursor()
#     cursor.execute('INSERT INTO user (first_name, last_name, email, phone_1, city, state) VALUES (%s, %s, %s, %s, %s, %s)', (first_name, last_name, email, phone_1, city, state))
#     db.get_db().commit()
#     user_id = cursor.lastrowid
#     the_response = make_response(jsonify({'user_id': user_id}), 201)
#     the_response.mimetype = 'application/json'
#     return the_response


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


    # # Add new caregiver
    # new_caregiver = data.get('new_caregiver')
    # if new_caregiver:
    #     name = new_caregiver.get('name')
    #     email = new_caregiver.get('email')
    #     password = new_caregiver.get('password')
    #     phone_number = new_caregiver.get('phone_number')
    #     address = new_caregiver.get('address')
    #     cursor = db.get_db().cursor()
    #     cursor.execute('INSERT INTO user (name, email, password, phone_number, address) VALUES (%s, %s, %s, %s, %s)', (name, email, password, phone_number, address))
    #     db.get_db().commit()
    #     caregiver_id = cursor.lastrowid
    #     cursor.execute('INSERT INTO caregiver (name, email, phone, user_id) VALUES (%s, %s, %s, %s)', (name, email, phone_number, caregiver_id))
    #     db.get_db().commit()

    # # Get updated caregiver data
    # cursor = db.get_db().cursor()
    # cursor.execute('SELECT id, name, email, phone FROM caregiver WHERE id = {0}'.format(user_id))
    # row_headers = [x[0] for x in cursor.description]
    # json_data = []
    # theData = cursor.fetchall()
    # for row in theData:
    #     json_data.append(dict(zip(row_headers, row)))


    #  cursor.execute('INSERT INTO user (name, email, password, phone_number, address) VALUES (%s, %s, %s, %s, %s)', (name, email, password, phone_number, address))

# delete something else?
# @caregivers.route('/user/<int:user_id>', methods=['DELETE'])
# def delete_user_caregiver(user_id):
#     # Delete an existing caregiver for the current user
#     #caregiver = Caregiver.query.filter_by(id=user_id, user_id=current_user.id).first()
#     # if not caregiver:
#     #     return jsonify(error='Caregiver not found!')
#     # db.session.delete(caregiver)
#     # db.session.commit()
#     # delete caregiver from database using cursor.execute
#     cursor = db.get_db().cursor()
#     cursor.execute('DELETE FROM user WHERE user_id = %s', (user_id))

#     return jsonify(message='Caregiver deleted successfully!')

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

# @caregivers.route('/supported-by', methods=['POST'])
# def create_supported_by():
#     try:
#         resource_id = request.json['resource_id']
#         user_id = request.json['user_id']
#         # check if both resource_id and user_id are present
#         if not resource_id or not user_id:
#             return jsonify({'error': 'Please provide both resource_id and user_id.'}), 400

#         # create a new supported_by entry
#         cursor = db.cursor()
#         sql = "INSERT INTO supported_by (resource_id, user_id) VALUES (%s, %s)"
#         val = (resource_id, user_id)
#         cursor.execute(sql, val)
#         db.commit()

#         return jsonify({'message': 'New entry added to supported_by table.'}), 201
#     except:
#         return jsonify({'error': 'Failed to create a new entry in supported_by table.'}), 500

# @caregivers.route('/meeting', methods=['POST'])
# def create_meeting():
#     try:
#         support_group_id = request.json['support_group_id']
#         # check if support_group_id is present
#         if not support_group_id:
#             return jsonify({'error': 'Please provide support_group_id.'}), 400

#         # create a new meeting entry
#         cursor.execute('INSERT INTO meeting (support_group_id) VALUES (%s)', (support_group_id,))
#         db.connection.commit()

#         return jsonify({'message': 'New entry added to meeting table.'}), 201
#     except:
#         return jsonify({'error': 'Failed to create a new entry in meeting table.'}), 500

# @caregivers.route('/meeting/<int:meeting_id>', methods=['DELETE'])
# def delete_meeting(meeting_id):
#     try:
#         # check if meeting_id exists in the database
#         meeting = Meeting.query.get_or_404(meeting_id)

#         # cancel the meeting from the database
#         db.session.delete(meeting)
#         db.session.commit()

#         return jsonify({'message': 'Meeting canceled successfully.'}), 200
#     except:
#         return jsonify({'error': 'Failed to cancel meeting.'}), 500


# Get all symptom names and ids
@caregivers.route('/symptoms', methods=['GET'])
def get_symptoms():
    #user_id = request.args.get('user_id')
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