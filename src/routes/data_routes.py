import json
from flask import Blueprint, request
from chart_handler import ChartHandler
from models.call import Call
from models.employee import Employee

calls_db = Call()
employees_db = Employee()
chart_handler = ChartHandler()

data_bp = Blueprint('data', __name__,
                    url_prefix='/data', template_folder='templates')

months = {"01": "January", "02": "February", "03": "March", "04": "April", "05": "May", "06": "June",
          "07": "July", "08": "August", "09": "September", "10": "October", "11": "November", "12": "December"}


@data_bp.route('/all-count', methods=["GET"])
def all_count():
    # args = request.args
    # print(args['time'])

    # get data and transform dates into string dates
    data = calls_db.get_total_calls_emails_counts()
    data_dict = {}
    for tuple in data:
        data_dict[months[tuple[0]]] = {
            "Total": tuple[1],
            "Calls": tuple[2],
            "Emails": tuple[3]
        }

    # define and return json response
    json_data = {
        "labels": [key for key in data_dict.keys()],
        "datasets": [
            {
                "label": "Call and Email Count",
                "backgroundColor": "rgb(70,60,220)",
                "borderColor": "rgb(70,60,220)",
                "data": get_concurrent_data(data_dict, "Total")
            },
            {
                "label": "Calls Count",
                "backgroundColor": "rgb(60,220,100)",
                "borderColor": "rgb(60,220,100)",
                "data": get_concurrent_data(data_dict, "Calls")
            },
            {
                "label": "Email Count",
                "backgroundColor": "rgb(240,190,50)",
                "borderColor": "rgb(240,190,50)",
                "data": get_concurrent_data(data_dict, "Emails")
            }
        ]
        
    }
    return json.dumps(json_data)


@data_bp.route('/all-count-sd', methods=["GET"])
def all_count_by_sub_dept():
    data = calls_db.get_calls_and_email_count_by_sub_dept()
    json_data = dict()
    for tuple in data:
        if tuple[0] not in json_data:
            json_data[tuple[0]] = {"H": 0, "S": 0, "O": 0}
        json_data[tuple[0]][tuple[1]] += tuple[2]
    


        

@data_bp.route('/imm_later_software', methods=["GET"])
def get_imm_later_software():
    data = calls_db.get_total_immediate_and_later_counts(sup_dept='S')
    json_data = dict()
    
    data_dict = {"Total":data[0][0], "Immediate":data[0][1], "Later":data[0][2]}

    json_data = {
        "labels":["Counts"],
        "datasets": [
            {
                "label": "Total",
                "backgroundColor": "rgb(70,60,220)",
                "borderColor": "rgb(70,60,220)",
                "data": [data_dict["Total"]]
            },
            {
                "label": "Immediate Count",
                "backgroundColor": "rgb(60,220,100)",
                "borderColor": "rgb(60,220,100)",
                "data":[data_dict["Immediate"]]
            },
            {
                "label": "Later Count",
                "backgroundColor": "rgb(240,190,50)",
                "borderColor": "rgb(240,190,50)",
                "data": [data_dict["Later"]]
            },
        ]
    }
    return json.dumps(json_data)

@data_bp.route('/imm_later_hardware', methods=["GET"])
def get_imm_later_hardware():
    data = calls_db.get_total_immediate_and_later_counts(sup_dept='H')
    json_data = dict()
    
    data_dict = {"Total":data[0][0], "Immediate":data[0][1], "Later":data[0][2]}

    json_data = {
        "labels":["Counts"],
        "datasets": [
            {
                "label": "Total",
                "backgroundColor": "rgb(70,60,220)",
                "borderColor": "rgb(70,60,220)",
                "data": [data_dict["Total"]]
            },
            {
                "label": "Immediate Count",
                "backgroundColor": "rgb(60,220,100)",
                "borderColor": "rgb(60,220,100)",
                "data": [data_dict["Immediate"]]
            },
            {
                "label": "Later Count",
                "backgroundColor": "rgb(240,190,50)",
                "borderColor": "rgb(240,190,50)",
                "data":[data_dict["Later"]]
            },
        ]
    }
    return json.dumps(json_data)

def get_concurrent_data(dict, column_name):
    concurrent_list = []
    for values in dict.values():
        concurrent_list.append(values[column_name])
    return concurrent_list
