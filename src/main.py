import os
from flask import Flask, redirect, render_template, request
from file_parsing.utility import createDependencies, createTempFiles
from models.employee import Employee
from file_parsing.parser import Parser

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/parse',  methods=["GET", "POST"])
def parse():
    if request.method == "GET":
        return render_template('parse.html')
    else:
        # create temp files
        daily = request.files['formFileDaily']
        all = request.files['formFileAll']
        createTempFiles(daily, all)

        # parse temp files
        parser = Parser()
        parser.parse_text("./data/temp/" + daily.filename)
        parser.parse_text("./data/temp/" + all.filename)

        return redirect('/')


@app.route('/sheets', methods=["GET", "POST"])
def sheets():
    if request.method == "GET":
        return render_template('sheets.html')
    


@app.route('/employees',  methods=["GET", "POST"])
def employees():
    emp_db = Employee()

    if request.method == "GET":
        return render_template('employees.html', employees=emp_db.read())
    elif request.method == "POST":
        employee = (
            request.form['id'],
            request.form['name'],
            request.form['sub_dept']
        )
        emp_db.insert(employee)
        return redirect('/employees')


if __name__ == '__main__':
    createDependencies(os.path)
    app.run(debug=True)
