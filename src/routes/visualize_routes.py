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
    software_table.generate_table()
    return render_template('visualize.html', software_table=software_table.table, employees=employees_db.read())
