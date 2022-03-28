import os
from flask import Flask, redirect, render_template, request
from utility import create_dependencies, create_temp_files
from models.employee import Employee
from models.call import Call
from report_parser import Parser

app = Flask(__name__)
calls_db = Call()
employees_db = Employee()


@app.route('/')
def index():
   #return str(employees_db.find_employee('U002Ryan'))
    return render_template('index.html')


@app.route('/parse',  methods=["GET", "POST"])
def parse():
    if request.method == "GET":
        return render_template('parse.html')
    else:
        # create temp files
        daily = request.files['formFileDaily']
        all = request.files['formFileAll']
        create_temp_files(daily, all)

        # parse temp files
        parser = Parser()
        parser.parse_text("./data/temp/" + daily.filename)
        parser.parse_text("./data/temp/" + all.filename)

        return redirect('/sheets')


@app.route('/sheets', methods=["GET"])
def sheets():
    return render_template('sheets.html', calls=calls_db.read(), employees=employees_db.read())

@app.route('/visualize', methods=["GET"])
def visualize():
    return render_template('visualize.html', calls=calls_db.read(), employees=employees_db.read())


@app.route('/employees',  methods=["GET", "POST"])
def employees():
    if request.method == "GET":
        return render_template('employees.html', employees=employees_db.read())
    elif request.method == "POST":
        employee = employees_db.build_employee(
            request.form['employee_id'],
            request.form['name'],
            request.form['sub_dept']
        )
        employees_db.insert(employee)
        return redirect('/employees')


if __name__ == '__main__':
    create_dependencies(os.path)
    app.run(debug=True)
