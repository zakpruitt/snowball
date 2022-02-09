from operator import index
import pandas as pd
from file_parser import FileParser


def generate_excel_file(information, count):
    # create dataframes
    columns = ['Date Created', 'Sup Code', 'Sub Dept', 'Email', 'Employee #',
               'Support #', 'Last User', 'Original User', 'Time Last Changed']
    info_df = pd.DataFrame(information, columns=columns)
    count_df = pd.DataFrame(count)

    # XLSX writer objects
    writer = pd.ExcelWriter("output.xlsx",
                            engine='xlsxwriter',
                            options={'strings_to_numbers': True})
    info_df.to_excel(writer, sheet_name='MaddenCo Data {Date}', index=False)
    count_df.to_excel(writer, sheet_name='MaddenCo Counts {Date}', index=True)
    workbook = writer.book
    info_worksheet = writer.sheets['MaddenCo Data {Date}']
    count_worksheet = writer.sheets['MaddenCo Counts {Date}']

    # formats
    blue_header_format = workbook.add_format(
        {'bg_color': '#5B9BD5', 'font': 'Calibri Light', 'font_size': '12', 'align': 'center',
         'border': 1})
    yellow_header_format = workbook.add_format(
        {'bg_color': '#FFC000', 'font': 'Calibri Light', 'font_size': '12', 'align': 'center',
         'border': 1})
    blue_format = workbook.add_format(
        {'bg_color': '#DDEBF7', 'font': 'Calibri Light', 'font_size': '12', 'align': 'center',
         'border': 1})
    yellow_format = workbook.add_format(
        {'bg_color': '#FFF2CC', 'font': 'Calibri Light', 'font_size': '12', 'align': 'center',
         'border': 1})

    # set info column headers
    for col_num, value in enumerate(info_df.columns.values):
        if col_num % 2 == 0:
            info_worksheet.write(0, col_num, value, blue_header_format)
        else:
            info_worksheet.write(0, col_num, value, yellow_header_format)

    # set info columns
    for col in range(0, 9):
        if col % 2 == 0:
            info_worksheet.set_column(col, col, 25, blue_format)
        else:
            info_worksheet.set_column(col, col, 25, yellow_format)

    # set count column headers
    for col_num, value in enumerate(count_df.columns.values):
        if col_num % 2 == 0:
            count_worksheet.write(0, col_num + 1, value, blue_header_format)
        else:
            count_worksheet.write(0, col_num + 1, value, yellow_header_format)

    for col_num, value in enumerate(count_df.index.values):
        count_worksheet.write(0, col_num + 1, value, blue_header_format)

    count_worksheet.write(0, 0, "Employee #", blue_header_format)
    for row in range(0, 4):
        value = count_df.index.values[row]
        count_worksheet.write(row + 1, 0, value, blue_header_format)

    for col in range(0, len(count_df.columns) + 1):
        count_worksheet.set_column(col, col, 25, blue_format)

    writer.save()


if __name__ == '__main__':
    file_parser = FileParser("./MaddenCo/20220106.txt")
    file_parser.parse_text()
    generate_excel_file(file_parser.get_information(), file_parser.get_count())
    print("done")
