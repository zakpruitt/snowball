from flask import Blueprint, request, render_template, redirect
from models.call import Call
from models.employee import Employee

calls_db = Call()
employees_db = Employee()

visualize_bp = Blueprint('visualize', __name__,
                      url_prefix='/visualize', template_folder='templates')


@visualize_bp.route('/', methods=["GET"])
def visualize():
    return render_template('visualize.html', calls=calls_db.read(), employees=employees_db.read())
