from flask import Blueprint, request, render_template, redirect
from models.call import Call
from models.employee import Employee

calls_db = Call()
employees_db = Employee()

data_bp = Blueprint('data', __name__,
                         url_prefix='/data', template_folder='templates')


@data_bp.route('/all-count', methods=["GET"])
def visualize():
    return render_template('visualize.html', calls=calls_db.read(), employees=employees_db.read())
