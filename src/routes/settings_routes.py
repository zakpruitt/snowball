from flask import Blueprint, request, render_template, redirect
from models.employee import Employee

employees_db = Employee()

settings_bp = Blueprint('settings', __name__,
                     url_prefix='/settings', template_folder='templates')


@settings_bp.route('/employees',  methods=["GET", "POST"])
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
