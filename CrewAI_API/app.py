import os
from flask import Flask, jsonify, request
import json


app = Flask(__name__)

def get_latest_file(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    if not files:
        return None

    latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(directory, f)))
    return os.path.join(directory, latest_file)


latest_json_file = ""
roles = ""
directory_path = "data_crew\src\data_crew\json_files\Python_Developer"

def run_app():
    print("Running app...")
    os.system("python data_crew\src\data_crew\main.py")
    global roles
    if os.path.exists(directory_path):
        global latest_json_file
        latest_json_file = os.path.relpath(get_latest_file(directory_path))
        print("file name = " + latest_json_file)
    with open(latest_json_file, 'r') as f:
        roles = json.load(f)
    app.run()



@app.route("/roles", methods=["GET"])
def get_roles():
    return roles

@app.route("/roles/<int:role_id>", methods=["GET"])
def get_role(role_id):
    if len(roles) < (role_id - 1):
        return jsonify({"error": "Role not found."}), 404
    else:
        return roles[role_id - 1]

@app.route("/roles", methods=["POST"])
def create_role():
    global roles
    new_role = {
        "ID" : str(int(roles[len(roles) - 1]["ID"]) + 1),
        "Job Role": "Senior Unreal Engine Developer",
        "Company Name": "Rockstar Games",
        "Job Title": "Senior Gameplay Programmer",
        "Job Description": "Lead developer role for large-scale games.",
        "Responsibilities": ["- Ensure the efficiency of application performance.",
                             "- Lead a team of developers for project completion."],
        "Qualifications and Skills": ["- Deep understanding of C++/Unreal Engine and related technologies.",
                                      "- Excellent debugging and problem-solving skills."],
        "Experience Required": "8+ years"
    }
    roles.append(new_role)
    with open(latest_json_file, "w") as f:
            json.dump(roles, f, indent=4)
    return roles[len(roles) - 1]

@app.route("/roles/<int:role_id>", methods=["PUT"])
def update_role(role_id):
    data = request.get_json()
    global roles
    if len(roles) < (role_id - 1):
        return jsonify({"error": "Role not found."}), 404
    else:
        role = roles[role_id - 1]
        role["Company Name"] = data.get("Company Name", role["Company Name"])
        role["Job Title"] = data.get("Job Title", role["Job Title"])
        role["Job Description"] = data.get("Job Description", role["Job Description"])
        role["Responsibilities"] = data.get("Responsibilities", role["Responsibilities"])
        role["Qualifications and Skills"] = data.get("Qualifications and Skills", role["Qualifications and Skills"])
        role["Experience Required"] = data.get("Experience Required", role["Experience Required"])
        with open(latest_json_file, "w") as f:
            json.dump(roles, f, indent=4)
        return roles[role_id - 1]

@app.route("/roles/<int:role_id>", methods=["DELETE"])
def delete_role(role_id):
    global roles
    if len(roles) < (role_id - 1):
        return jsonify({"error": "Role not found."}), 404
    else:
        new_roles_list = list(filter(lambda r : r["ID"] != role_id, roles))
        roles = new_roles_list
        with open(latest_json_file, "w") as f:
            json.dump(roles, f, indent=4)
        return roles

run_app()
