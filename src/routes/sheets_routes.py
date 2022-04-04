from flask import Blueprint, request, render_template
from models.call import Call
from models.employee import Employee

calls_db = Call()
employees_db = Employee()

sheets_bp = Blueprint('sheets', __name__, url_prefix='/sheets',
                      template_folder='templates')


@sheets_bp.route('/', methods=["GET"])
def sheets():
    return render_template('sheets.html', calls=calls_db.read(), employees=employees_db.read())
