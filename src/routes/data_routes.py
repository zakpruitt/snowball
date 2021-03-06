import json
from flask import Blueprint, request
from chart_handler import ChartHandler
from models.call import Call
from models.employee import Employee
from PIL import ImageColor

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
        data_dict[tuple[0]] = {
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


@data_bp.route('/bar-data', methods=["GET"])
def bar_data():
    start = request.args.get('start')
    end = request.args.get('end')
    sub_dept = request.args.get('sub_dept')

    # get data and transform dates into string dates
    data = calls_db.get_total_calls_and_email_count_by_employee(
        start, end, sub_dept)

    data_dict = {}
    for tuple in data:
        data_dict[tuple[0]] = {
            "Total": tuple[1],
            "Calls": tuple[2],
            "Emails": tuple[3]
        }

    # define and return json response
    json_data = {
        "labels": [key for key in data_dict],
        "datasets": [
            {
                "label": "Total",
                "backgroundColor": chart_handler.preset_color("Total"),
                "borderColor": chart_handler.preset_color("Total"),
                "data": [data_dict[key]["Total"] for key in data_dict]
            },
            {
                "label": "Calls",
                "backgroundColor": chart_handler.preset_color("Calls"),
                "borderColor": chart_handler.preset_color("Calls"),
                "data": [data_dict[key]["Calls"] for key in data_dict]
            },
            {
                "label": "Emails",
                "backgroundColor": chart_handler.preset_color("Emails"),
                "borderColor": chart_handler.preset_color("Emails"),
                "data": [data_dict[key]["Emails"] for key in data_dict]
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


@data_bp.route('/pie-email-data', methods=["GET"])
def get_pie_email_data():
    # retrieve data from db
    start = request.args.get('start')
    end = request.args.get('end')
    sub_dept = request.args.get('sub_dept')
    data = calls_db.get_email_counts_per_employee(start, end, sub_dept)

    # build data dict
    data_dict = dict()
    label = "Emails Dataset"
    for tuple in data:
        data_dict[tuple[0]] = tuple[1]
    employees = [key for key in data_dict.keys() if data_dict[key] > 0]
    json_data = {
        "labels": employees,
        "datasets": [
            {
                "label": label,
                "backgroundColor": [],
                "borderColor": [],
                "data": [value for value in data_dict.values() if value > 0]
            }
        ]
    }

    # populate colors
    chart_handler.map_employees(employees)
    for employee in json_data["labels"]:
        color = employees_db.get_color_by_name(employee)
        color = ImageColor.getcolor(color, "RGB")
        color += (0.7,)
        json_data["datasets"][0]["backgroundColor"].append("rgba" + str(color))
        json_data["datasets"][0]["borderColor"].append("rgba" + str(color))

    # return chart json
    return json.dumps(json_data)


@data_bp.route('/pie-data', methods=["GET"])
def get_pie_data():
    # retrieve data from database
    sub_dept = request.args.get('sub_dept')
    category = request.args.get('category')
    start = request.args.get('start')
    end = request.args.get('end')
    data = calls_db.get_immediate_and_later_count_per_employee(
        start, end, sub_dept)

    # create dict
    data_dict = dict()
    if category == 'imm':
        label = 'Immediate Calls Dataset'
        for tuple in data:
            data_dict[tuple[0]] = tuple[2]
    elif category == 'later':
        label = 'Later Calls Dataset'
        for tuple in data:
            data_dict[tuple[0]] = tuple[3]
    employees = [key for key in data_dict.keys() if data_dict[key] > 0]

    # create json response
    json_data = {
        "labels": employees,
        "datasets": [
            {
                "label": label,
                "backgroundColor": [],
                "borderColor": [],
                "data": [value for value in data_dict.values() if value > 0]
            }
        ]
    }

    # populate colors
    for employee in json_data["labels"]:
        color = employees_db.get_color_by_name(employee)
        color = ImageColor.getcolor(color, "RGB")
        color += (0.7,)
        json_data["datasets"][0]["backgroundColor"].append("rgba" + str(color))
        json_data["datasets"][0]["borderColor"].append("rgba" + str(color))

    # return chart json
    return json.dumps(json_data)


def get_concurrent_data(dict, column_name):
    concurrent_list = []
    for values in dict.values():
        concurrent_list.append(values[column_name])
    return concurrent_list

