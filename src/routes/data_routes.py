import json
from flask import Blueprint, request
from models.call import Call
from models.employee import Employee

calls_db = Call()
employees_db = Employee()

data_bp = Blueprint('data', __name__,
                    url_prefix='/data', template_folder='templates')

months = {"01": "January", "02": "February", "03": "March", "04": "April", "05": "May", "06": "June",
          "07": "July", "08": "August", "09": "September", "10": "October", "11": "November", "12": "December"}


@data_bp.route('/all-count', methods=["GET"])
def all_count():
    data = dict(calls_db.get_calls_and_email_count())
    for key in data.copy().keys():
        data[months[key]] = data.pop(key)
    return json.dumps(data)
