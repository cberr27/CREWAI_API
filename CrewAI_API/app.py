import os
from flask import Flask, jsonify, redirect, render_template, request
import json
from data_crew.src.data_crew import main


app = Flask(__name__)

def get_latest_file(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    if not files:
        return None

    latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(directory, f)))
    return os.path.join(directory, latest_file)


latest_json_file = ""
roles = ""
folder_name = "Python_Developer"
directory_path = f"data_crew\src\data_crew\json_files\{folder_name}"


def run_app():
    print("Running app...")
    #main.run()
    global roles
    if os.path.exists(directory_path):
        global latest_json_file
        latest_json_file = os.path.relpath(get_latest_file(directory_path))
        print("file name = " + latest_json_file)
    with open(latest_json_file, 'r') as f:
        roles = json.load(f)
    app.run()



@app.route("/", methods=["GET"])
def get_home():
    return render_template("index.html")

@app.route("/roles", methods=["GET"])
def get_roles():
    return roles

@app.route("/roles/<int:role_id>", methods=["GET"])
def get_role(role_id):
    if len(roles) < (role_id - 1):
        return jsonify({"error": "Role not found."}), 404
    else:
        return roles[role_id - 1]

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
    
@app.route("/fetch_roles", methods=["GET", "POST"])
def fetch_form():
    if request.method == "POST":
        try:
            job_role = request.form.get("job_role")
            folder_name = main.change_topic(job_role)
            directory_path = f"data_crew\src\data_crew\json_files\{folder_name}"
        except KeyError:
            return "Error: 'job_role' key not found in the form data"
        main.run()
        global roles
        if os.path.exists(directory_path):
            global latest_json_file
            latest_json_file = os.path.relpath(get_latest_file(directory_path))
            print("file name = " + latest_json_file)
        with open(latest_json_file, 'r') as f:
            roles = json.load(f)
        return redirect("/roles")
    return render_template("fetch_roles.html")

@app.route("/add_role", methods=["GET", "POST"])
def add_form():
    if request.method == "POST":
        # Get Data From Form
        try:
            company_name = request.form.get("company_name")
        except KeyError:
            return "Error: 'company_name' key not found in the form data"
        try:
            job_title = request.form["job_title"]        
        except KeyError:
            return "Error: 'job_title' key not found in the form data"
        try:
            job_description = request.form["job_description"]
        except KeyError:
            return "Error: 'job_description' key not found in the form data"
        try:
            responsibilites = request.form["responsibilites"]       
        except KeyError:
            return "Error: 'responsibilites' key not found in the form data"
        try:
            qualifications = request.form["qualifications"]        
        except KeyError:
            return "Error: 'qualifications' key not found in the form data"
        try:
            experience = request.form["experience_required"]
        except KeyError:
            return "Error: 'experience' key not found in the form data"
        
        # Add Data From Form To JSON file
        global roles
        new_role = {
        "ID" : int(roles[len(roles) - 1]["ID"]) + 1,
        "Company Name": company_name,
        "Job Title": job_title,
        "Job Description": job_description,
        "Responsibilities": responsibilites,
        "Qualifications and Skills": qualifications,
        "Experience Required": experience
        }
        roles.append(new_role)
        with open(latest_json_file, "w") as f:
                json.dump(roles, f, indent=4)
        return redirect("/roles")
    return render_template("add_role.html")


run_app()
