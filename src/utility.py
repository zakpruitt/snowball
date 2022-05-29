import json
import os
import ntpath
import datetime
import random


def create_dependencies(path):
    if not path.exists('./data/temp'):
        os.makedirs('./data/temp')


def create_temp_files(*args):
    for file in args:
        file.save("./data/temp/" + file.filename)


def get_file_date(file_path):
    date = ntpath.basename(file_path)[:8]
    formatted_date = date[4:6] + '-' + date[6:] + '-' + date[0:4]  # mm-dd-yyyy
    return formatted_date


def get_date_time():
    return datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")


def write_format_json():
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
