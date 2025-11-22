from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# -------------------------
# Base directory (Windows-safe)
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, 'database')

# -------------------------
# Helper functions to load/save JSON
# -------------------------
def load_json(filename):
    path = os.path.join(DB_DIR, filename)
    if not os.path.exists(path):
        # Initialize empty list if file doesn't exist
        with open(path, 'w') as f:
            json.dump([], f)
    with open(path, 'r') as file:
        return json.load(file)

def save_json(filename, data):
    path = os.path.join(DB_DIR, filename)
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

# -------------------------
# GET ALL PATIENTS
# -------------------------
@app.route('/patients', methods=['GET'])
def get_patients():
    data = load_json('patients.json')
    return jsonify(data)

# -------------------------
# ADD A NEW PATIENT
# -------------------------
@app.route('/patients', methods=['POST'])
def add_patient():
    patients = load_json('patients.json')
    new_patient = request.json

    # Auto-assign ID
    new_patient['id'] = patients[-1]['id'] + 1 if patients else 1

    # Set default values if not provided
    new_patient.setdefault('priority', 0)
    new_patient.setdefault('status', 'waiting')

    patients.append(new_patient)
    save_json('patients.json', patients)

    return jsonify({"message": "Patient added!", "patient": new_patient}), 201

# -------------------------
# GET ALL DOCTORS
# -------------------------
@app.route('/doctors', methods=['GET'])
def get_doctors():
    data = load_json('doctors.json')
    return jsonify(data)

# -------------------------
# ADD A NEW DOCTOR
# -------------------------
@app.route('/doctors', methods=['POST'])
def add_doctor():
    doctors = load_json('doctors.json')
    new_doc = request.json

    # Auto-assign ID
    new_doc['id'] = doctors[-1]['id'] + 1 if doctors else 1

    # Set default availability
    new_doc.setdefault('availability', 'available')

    doctors.append(new_doc)
    save_json('doctors.json', doctors)

    return jsonify({"message": "Doctor added!", "doctor": new_doc}), 201

# -------------------------
# SERVE A PATIENT (assign doctor)
# -------------------------
@app.route('/serve', methods=['POST'])
def serve_patient():
    served_list = load_json('served_patients.json')
    entry = request.json  # { "patient_id": 1, "doctor_id": 2 }

    # Optional: mark patient as done
    patients = load_json('patients.json')
    for p in patients:
        if p['id'] == entry['patient_id']:
            p['status'] = 'done'
    save_json('patients.json', patients)

    served_list.append(entry)
    save_json('served_patients.json', served_list)

    return jsonify({"message": "Patient served!", "data": entry}), 201

# -------------------------
# RUN SERVER
# -------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
