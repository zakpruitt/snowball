from flask import Blueprint, request, render_template, redirect
from models.employee import Employee

employees_db = Employee()

settings_bp = Blueprint('settings', __name__,
                        url_prefix='/settings', template_folder='templates')


@settings_bp.route("/", methods=['GET', 'POST'])
def settings():
    if request.method == "GET":
        return render_template('settings.html', employees=employees_db.read(), color=get_random_color())
    elif request.method == "POST":
        employee = tuple(request.form.values())
        employees_db.insert(employee)
        return redirect('/settings')


@settings_bp.route("/delete", methods=['POST'])
def delete_employee():
    employee_id = request.form.get('id')
    employees_db.delete(employee_id)
    return redirect('/settings')


def get_random_color():
    import random
    hexadecimal = "#" + \
        ''.join([random.choice('ABCDEF0123456789') for i in range(6)])
    return hexadecimal
