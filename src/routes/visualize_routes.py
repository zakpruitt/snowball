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
    hardware_table = TableHandler(sub_dept="H")
    hardware_table.generate_table()
    other_table = TableHandler(sub_dept="O")
    other_table.generate_table()

    random_table = TableHandler(start="2022-01-04", end="2022-02-14", sub_dept="O")
    random_table.generate_table()

    return render_template(
        'visualize.html', 
        software_table=software_table.table, 
        hardware_table=hardware_table.table,
        other_table=other_table.table,
        employees=employees_db.read()
    )
