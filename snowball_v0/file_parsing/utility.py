import json
import os
import ntpath
import datetime


def createDependencies(path):
    if not path.exists('generated'):
        os.makedirs('./generated')
    if not path.exists('config'):
        os.makedirs('./config')
        writeFormatJSON()
        writeEmployeeJSON()


def writeFormatJSON():
    with open("./config/excel_formats.json", 'w') as f:
        json.dump({
            "formats": [
                {
                    "name": "blue_header_format",
                    "bg_color": "#5B9BD5",
                    "font": "Calibri Light",
                    "font_size": "12",
                    "align": "center",
                    "border": 1
                },

                {
                    "name": "yellow_header_format",
                    "bg_color": "#FFC000",
                    "font": "Calibri Light",
                    "font_size": "12",
                    "align": "center",
                    "border": 1
                },

                {
                    "name": "blue_format",
                    "bg_color": "#DDEBF7",
                    "font": "Calibri Light",
                    "font_size": "12",
                    "align": "center",
                    "border": 1
                },
                {
                    "name": "yellow_format",
                    "bg_color": "#FFF2CC",
                    "font": "Calibri Light",
                    "font_size": "12",
                    "align": "center",
                    "border": 1
                },
                {
                    "name": "cyan_header_format",
                    "bg_color": "#4BACC6",
                    "font": "Calibri Light",
                    "font_size": "12",
                    "align": "center",
                    "border": 1
                },
                {
                    "name": "orange_header_format",
                    "bg_color": "#F79646",
                    "font": "Calibri Light",
                    "font_size": "12",
                    "align": "center",
                    "border": 1
                },
                {
                    "name": "cyan_format",
                    "bg_color": "#DAEEF3",
                    "font": "Calibri Light",
                    "font_size": "12",
                    "align": "center",
                    "border": 1
                },
                {
                    "name": "orange_format",
                    "bg_color": "#FDE9D9",
                    "font": "Calibri Light",
                    "font_size": "12",
                    "align": "center",
                    "border": 1
                }
            ]
        }, f)


def writeEmployeeJSON():
    with open("./config/employees.json", 'w') as f:
        json.dump(
            {
                "115": "U002RHONDA",
                "107": "U002SUSIE",
                "142": "U002JEREMY",
                "154": "U002SEAN",
                "161": "U002RYANW",
                "138": "U002MICHELLE",
                "124": "U002RYAN",
                "169": "U002SUZANN",
                "170": "U002BETHAN",
                "155": "U002STACI",
                "158": "U002RYLAN",
                "149": "U002MAGGIE",
                "123": "U002DENNY",
                "90": "U002DANA",
                "153": "U002RICH",
                "95": "U002KIM",
                "162": "U002MIKE"
            }, f)


def getFileDate(file_path):
    date = ntpath.basename(file_path)[:8]
    formatted_date = date[4:6] + '-' + date[6:] + '-' + date[0:4]  # mm-dd-yyyy
    return formatted_date


def getDateTime():
    return datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
