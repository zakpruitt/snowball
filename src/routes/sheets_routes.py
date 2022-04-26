from flask import Blueprint, request, render_template, redirect
from models.call import Call
from models.employee import Employee

calls_db = Call()
employees_db = Employee()

sheets_bp = Blueprint('sheets', __name__, url_prefix='/sheets',
                      template_folder='templates')


@sheets_bp.route('/', methods=["GET"])
def sheets():
    return render_template('sheets.html', calls=calls_db.read(), employees=employees_db.read())


@sheets_bp.route('/delete', methods=["POST"])
def delete_call():
    date = request.form["callNumber"]
    sup_num = request.form["dateCreated"]
    print(date + " " + sup_num)
    calls_db.delete(date, sup_num)
    return redirect('/sheets')
