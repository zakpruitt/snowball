import pandas as pd
import xlwings as xw

from file_parsing.parser import Parser
from file_parsing.excel_writer import ExcelWriter
from datetime import date

if __name__ == '__main__':
    # parse text file(s)
    file_parser = Parser("./file_parsing/20220106.txt")
    file_parser.parse_text()

    # create excel_writer object and dataframes
    excel_writer = ExcelWriter("output.xlsx")
    columns = ['Date Created', 'Sup Code', 'Sub Dept', 'Email', 'Employee #',
               'Support #', 'Last User', 'Original User', 'Time Last Changed']
    info_df = pd.DataFrame(file_parser.line_information, columns=columns)
    count_df = pd.DataFrame(file_parser.count_information)

    # create and write new sheets
    today = date.today()
    formatted_date = today.strftime("%m-%d-%Y")
    excel_writer.create_and_write_new_sheet(
        f"MaddenCo Data {formatted_date}", info_df)
    excel_writer.create_and_write_new_sheet(
        f"MaddenCo Count {formatted_date}", count_df, True)

    # create formats
    excel_writer.create_format(
        "blue_header_format", '#5B9BD5', 'Calibri Light', '12', 'center', 1)
    excel_writer.create_format(
        "yellow_header_format", '#FFC000', 'Calibri Light', '12', 'center', 1)
    excel_writer.create_format(
        "blue_format", '#DDEBF7', 'Calibri Light', '12', 'center', 1)
    excel_writer.create_format(
        "yellow_format", '#FFF2CC', 'Calibri Light', '12', 'center', 1)
    excel_writer.create_format(
        "cyan_header_format", "#4BACC6", 'Calibri Light', '12', 'center', 1)
    excel_writer.create_format(
        "orange_header_format", "#F79646", 'Calibri Light', '12', 'center', 1)
    excel_writer.create_format(
        "cyan_format", "#DAEEF3", 'Calibri Light', '12', 'center', 1)
    excel_writer.create_format(
        "orange_format", "#FDE9D9", 'Calibri Light', '12', 'center', 1)

    # format sheets
    excel_writer.format_headers_af(
        f"MaddenCo Data {formatted_date}", info_df, 0, "blue_header_format", "yellow_header_format")
    excel_writer.format_columns_af(
        f"MaddenCo Data {formatted_date}", info_df, 0, 25, "blue_format", "yellow_format")
    excel_writer.format_headers_af(
        f"MaddenCo Count {formatted_date}", count_df, 1, "cyan_header_format", "orange_header_format")
    excel_writer.format_columns_af(
        f"MaddenCo Count {formatted_date}", count_df, 1, 25, "cyan_format", "orange_format")
    excel_writer.format_row_index(
        f"MaddenCo Count {formatted_date}", count_df, "cyan_header_format")

    # save
    excel_writer.writer.save()

    wb = xw.Book('master.xlsm')
    print(wb.Range('A1').current_region.last_cell.row)
    print(wb.sheets["DATA"]['Q1'].value)

    print("Done!")
