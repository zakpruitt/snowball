import json
import os

def createDependencies(path):
    if not path.exists('generated'):
        os.makedirs('./generated')
    if not path.exists('config'):
        os.makedirs('./config')
        writeFormatJSON()


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
