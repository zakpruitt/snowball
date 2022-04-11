from msilib import Table
from flask import Blueprint, request, render_template, redirect
from models.call import Call
from models.employee import Employee
from table_handler import TableHandler

calls_db = Call()
employees_db = Employee()

visualize_bp = Blueprint('visualize', __name__,
                         url_prefix='/visualize', template_folder='templates')


@visualize_bp.route('/', methods=["GET"])
def visualize():
    software_table = TableHandler(sub_dept="S")
    return str(software_table.totals)

    return render_template('visualize.html', calls=calls_db.read(), employees=employees_db.read())
